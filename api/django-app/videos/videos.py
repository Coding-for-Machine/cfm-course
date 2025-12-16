import os
import tempfile
import subprocess
from celery import shared_task
from django.core.files.base import ContentFile
from django.conf import settings
import boto3
from botocore.exceptions import ClientError

VIDEO_QUALITIES = [
    {'name': '360p', 'width': 640, 'height': 360, 'bitrate': '800k'},
    {'name': '720p', 'width': 1280, 'height': 720, 'bitrate': '2800k'},
]

def get_s3_client():
    return boto3.client(
        's3',
        endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )

def generate_thumbnail(video_path, output_path, timestamp='00:00:01'):
    cmd = [
        'ffmpeg', '-i', video_path,
        '-ss', timestamp, '-vframes', '1',
        '-vf', 'scale=640:-1', '-q:v', '2',
        output_path, '-y'
    ]
    subprocess.run(cmd, check=True, capture_output=True)

def convert_to_hls(input_path, output_dir, qualities=VIDEO_QUALITIES):
    os.makedirs(output_dir, exist_ok=True)
    master_playlist = "#EXTM3U\n#EXT-X-VERSION:3\n\n"
    for q in qualities:
        q_dir = os.path.join(output_dir, q['name'])
        os.makedirs(q_dir, exist_ok=True)
        playlist_file = os.path.join(q_dir, f"{q['name']}.m3u8")
        segment_pattern = os.path.join(q_dir, f"{q['name']}_%03d.ts")
        cmd = [
            'ffmpeg', '-i', input_path,
            '-vf', f"scale={q['width']}:{q['height']}",
            '-c:v', 'libx264', '-preset', 'veryfast', '-b:v', q['bitrate'],
            '-c:a', 'aac', '-b:a', '128k',
            '-hls_time', '6', '-hls_list_size', '0',
            '-hls_segment_filename', segment_pattern,
            playlist_file
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        bandwidth = int(q['bitrate'].replace('k',''))*1000
        master_playlist += f"#EXT-X-STREAM-INF:BANDWIDTH={bandwidth},RESOLUTION={q['width']}x{q['height']}\n"
        master_playlist += f"{q['name']}/{q['name']}.m3u8\n\n"
    master_path = os.path.join(output_dir, 'master.m3u8')
    with open(master_path, 'w') as f:
        f.write(master_playlist)
    return master_path

def upload_dir_to_s3(local_dir, s3_prefix, bucket='media'):
    s3 = get_s3_client()
    uploaded_files = []
    for root, _, files in os.walk(local_dir):
        for file in files:
            local_path = os.path.join(root, file)
            rel_path = os.path.relpath(local_path, local_dir).replace("\\","/")
            s3_path = f"{s3_prefix}/{rel_path}"
            content_type = 'application/x-mpegURL' if file.endswith('.m3u8') else 'video/MP2T'
            s3.upload_file(local_path, bucket, s3_path, ExtraArgs={'ContentType': content_type, 'ACL':'public-read'})
            uploaded_files.append(s3_path)
    return uploaded_files

@shared_task(bind=True, max_retries=3)
def process_video(self, video_id, model_name='problems.Problem'):
    from django.apps import apps
    try:
        Model = apps.get_model(model_name)
        video_obj = Model.objects.get(id=video_id)
        video_obj.processing_status = 'processing'
        video_obj.save(update_fields=['processing_status'])

        if not video_obj.video:
            raise ValueError("Video file not found")

        s3 = get_s3_client()
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        s3.download_fileobj('media', video_obj.video.name, tmp_file)
        tmp_file.close()

        # Thumbnail
        thumb_path = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg").name
        generate_thumbnail(tmp_file.name, thumb_path)
        with open(thumb_path, 'rb') as f:
            video_obj.thumbnail.save(f"thumb_{video_id}.jpg", ContentFile(f.read()), save=True)
        os.unlink(thumb_path)

        # HLS
        tmp_dir = tempfile.mkdtemp()
        master_playlist = convert_to_hls(tmp_file.name, tmp_dir)
        uploaded_files = upload_dir_to_s3(tmp_dir, f"videos/hls/{video_id}")
        video_obj.hls_playlist = f"videos/hls/{video_id}/master.m3u8"
        video_obj.processing_status = 'completed'
        video_obj.save()

        # Cleanup
        os.unlink(tmp_file.name)
        import shutil; shutil.rmtree(tmp_dir)

    except Exception as e:
        video_obj.processing_status = 'failed'
        video_obj.processing_error = str(e)
        video_obj.save()
        raise self.retry(exc=e, countdown=60)
