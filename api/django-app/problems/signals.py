from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from .models import Video
from .tasks import process_video

@receiver(post_save, sender=Video)
def video_post_save_handler(sender, instance, created, **kwargs):
    if created and instance.original_file:
        transaction.on_commit(lambda: process_video.delay(instance.id))
