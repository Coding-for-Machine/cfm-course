import os
import subprocess
import ffmpeg
from celery import shared_task
from django.utils import timezone
from django.core.files.base import ContentFile
import boto3
from botocore.exceptions import ClientError
import tempfile
from django.conf import settings
from .models import Video, VideoQuality

VIDEO_QUALITIES = [
    {'name': '360p', 'width': 640, 'height': 360, 'bitrate': '800k'},
    {'name': '720p', 'width': 1280, 'height': 720, 'bitrate': '2800k'},
]

def get_s3_client():
    """MinIO/S3 client"""
    return boto3.client(
        's3',
        endpoint_url=getattr(settings, 'AWS_S3_ENDPOINT_URL', 'http://localhost:9000'),
        aws_access_key_id=getattr(settings, 'AWS_ACCESS_KEY_ID', 'minioadmin'),
        aws_secret_access_key=getattr(settings, 'AWS_SECRET_ACCESS_KEY', 'minioadmin123'),
        region_name=getattr(settings, 'AWS_S3_REGION_NAME', 'us-east-1')
    )

def get_video_info(video_path):
    """Video ma'lumotlarini olish"""
    try:
        probe = ffmpeg.probe(video_path)
        video_stream = next((s for s in probe['streams'] if s['codec_type'] == 'video'), None)
        if not video_stream:
            raise ValueError("Video stream topilmadi")
        return {
            'duration': float(probe['format']['duration']),
            'width': int(video_stream['width']),
            'height': int(video_stream['height']),
            'fps': eval(video_stream['r_frame_rate']),
            'bitrate': int(probe['format'].get('bit_rate', 0)),
            'codec': video_stream['codec_name'],
            'file_size': int(probe['format']['size'])
        }
    except Exception as e:
        raise Exception(f"Video info olishda xato: {str(e)}")

def generate_thumbnail(video_path, output_path, timestamp='00:00:01'):
    """Video'dan thumbnail yaratish"""
    try:
        (
            ffmpeg.input(video_path, ss=timestamp)
                  .filter('scale', 640, -1)
                  .output(output_path, vframes=1, format='image2', vcodec='mjpeg')
                  .overwrite_output()
                  .run(capture_stdout=True, capture_stderr=True, quiet=True)
        )
        return True
    except ffmpeg.Error as e:
        print(f"Thumbnail xato: {e.stderr.decode()}")
        return False

def convert_to_hls(input_path, output_dir, video_id, qualities):
    """Video'ni HLS formatiga o'tkazish - multi-quality"""
    os.makedirs(output_dir, exist_ok=True)
    master_playlist_path = os.path.join(output_dir, 'master.m3u8')
    master_content = "#EXTM3U\n#EXT-X-VERSION:3\n\n"
    processed_qualities = []

    for q in qualities:
        quality_dir = os.path.join(output_dir, q['name'])
        os.makedirs(quality_dir, exist_ok=True)
        playlist_file = os.path.join(quality_dir, f"{q['name']}.m3u8")
        segment_pattern = os.path.join(quality_dir, f"{q['name']}_%03d.ts")

        cmd = [
            'ffmpeg', '-i', input_path,
            '-vf', f"scale={q['width']}:{q['height']}",
            '-c:v', 'libx264', '-preset', 'veryfast', '-profile:v', 'main',
            '-b:v', q['bitrate'], '-maxrate', q['bitrate'],
            '-bufsize', f"{int(q['bitrate'].replace('k',''))*2}k",
            '-c:a', 'aac', '-b:a', '128k', '-ac', '2', '-ar', '48000',
            '-hls_time', '2', '-hls_init_time', '2', '-hls_allow_cache', '0',
            '-hls_playlist_type', 'event',
            '-hls_flags', 'independent_segments+program_date_time+delete_segments',
            '-hls_segment_filename', segment_pattern,
            '-hls_list_size', '5',
            playlist_file
        ]

        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            bandwidth = int(q['bitrate'].replace('k','')) * 1000
            master_content += f"#EXT-X-STREAM-INF:BANDWIDTH={bandwidth},RESOLUTION={q['width']}x{q['height']}\n"
            master_content += f"{q['name']}/{q['name']}.m3u8\n\n"

            processed_qualities.append({
                'quality': q['name'],
                'width': q['width'],
                'height': q['height'],
                'bitrate': q['bitrate'],
                'playlist': f"{q['name']}/{q['name']}.m3u8"
            })
        except subprocess.CalledProcessError as e:
            print(f"FFmpeg xato ({q['name']}): {e.stderr}")

    with open(master_playlist_path, 'w') as f:
        f.write(master_content)
    return processed_qualities

def upload_directory_to_s3(local_dir, s3_prefix, bucket='media'):
    """Directory'ni S3 ga yuklash"""
    s3_client = get_s3_client()
    uploaded_files = []
    for root, _, files in os.walk(local_dir):
        for file in files:
            local_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_path, local_dir)
            s3_path = os.path.join(s3_prefix, relative_path).replace('\\', '/')
            content_type = 'application/x-mpegURL' if file.endswith('.m3u8') else 'video/MP2T'
            try:
                s3_client.upload_file(local_path, bucket, s3_path,
                    ExtraArgs={'ContentType': content_type, 'ACL': 'public-read'})
                uploaded_files.append(s3_path)
            except Exception as e:
                print(f"Upload xato ({s3_path}): {e}")
    return uploaded_files

@shared_task(bind=True)
def process_video(self, video_id):
    """Asosiy video processing task"""
    try:
        video = Video.objects.get(id=video_id)
        video.status = 'processing'
        video.processing_progress = 0
        video.save()

        if not video.original_file:
            raise ValueError("Video fayl topilmadi")

        file_key = video.original_file.name
        s3_client = get_s3_client()
        s3_client.head_object(Bucket='media', Key=file_key)

        # Faylni yuklab olish
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
            s3_client.download_fileobj('media', file_key, tmp_file)
            tmp_file_path = tmp_file.name

        # Video info
        video_info = get_video_info(tmp_file_path)
        video.duration = video_info['duration']
        video.width = video_info['width']
        video.height = video_info['height']
        video.fps = video_info['fps']
        video.bitrate = video_info['bitrate']
        video.codec = video_info['codec']
        video.file_size = video_info['file_size']
        video.save()

        # Thumbnail yaratish
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as thumb_file:
            thumb_path = thumb_file.name
        if generate_thumbnail(tmp_file_path, thumb_path):
            with open(thumb_path, 'rb') as f:
                video.thumbnail.save(f'thumb_{video_id}.jpg', ContentFile(f.read()), save=True)
            os.unlink(thumb_path)

        # HLS ga o'tkazish
        max_height = video.height
        qualities_to_process = [q for q in VIDEO_QUALITIES if q['height'] <= max_height] or [VIDEO_QUALITIES[0]]
        with tempfile.TemporaryDirectory() as tmp_dir:
            processed_qualities = convert_to_hls(tmp_file_path, tmp_dir, video_id, qualities_to_process)
            s3_prefix = f'videos/hls/{video_id}'
            upload_directory_to_s3(tmp_dir, s3_prefix)
            video.hls_playlist = f'{s3_prefix}/master.m3u8'
            video.save()

            # VideoQuality yaratish
            for q in processed_qualities:
                VideoQuality.objects.update_or_create(
                    video=video,
                    quality=q['quality'],
                    defaults={
                        'width': q['width'],
                        'height': q['height'],
                        'bitrate': q['bitrate'],
                        'file_path': f"{s3_prefix}/{q['playlist']}",
                        'is_ready': True
                    }
                )

        os.unlink(tmp_file_path)
        video.status = 'completed'
        video.processing_progress = 100
        video.processed_at = timezone.now()
        video.save()

        return {'status': 'success', 'video_id': str(video_id), 'hls_url': video.get_hls_url()}

    except Exception as e:
        print(f"❌ Xato: {str(e)}")
        video.status = 'failed'
        video.processing_error = str(e)
        video.save()
        raise
