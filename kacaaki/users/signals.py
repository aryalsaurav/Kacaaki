from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

import os
import subprocess
import logging
import time

from moviepy.editor import VideoFileClip, clips_array

from .models import VideoUpload
from .tasks import convert_and_merge_videos,hello

logger = logging.getLogger(__name__)

@receiver(post_save, sender=VideoUpload)
def handel_merge(sender, instance, created, *args, **kwargs):
    if created:
        logger.info(f"Signal triggered for VideoUpload {instance.id}")
        convert_and_merge_videos.delay(instance.id)
        # hello.delay(instance.id)
        