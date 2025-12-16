from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class MediaStorage(S3Boto3Storage):
    """
    MinIO storage for media files (videos, images, thumbnails)
    """
    bucket_name = 'media'
    location = ''  # Root of bucket
    default_acl = 'public-read'
    file_overwrite = False
    custom_domain = None
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.info(f"✅ MediaStorage initialized: bucket={self.bucket_name}")
    
    def url(self, name):
        if not name:
            return ''
        name = self._normalize_name(name)
        return f"{settings.AWS_S3_ENDPOINT_URL}/{self.bucket_name}/{name}"
    

class StaticStorage(S3Boto3Storage):
    """
    MinIO storage for static files
    """
    bucket_name = 'static'
    location = ''
    default_acl = 'public-read'
    file_overwrite = True  # Static files can be overwritten
    custom_domain = None
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.info(f"✅ StaticStorage initialized: bucket={self.bucket_name}")
    
    def url(self, name):
        if not name:
            return ''
        name = self._normalize_name(name)
        return f"{settings.AWS_S3_ENDPOINT_URL}/{self.bucket_name}/{name}"