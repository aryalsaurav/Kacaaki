from celery import shared_task
from django.conf import settings

import os
import subprocess
import logging
import time
import random

from moviepy.editor import VideoFileClip, clips_array

from .models import VideoUpload,OPT,User


logger = logging.getLogger(__name__)



@shared_task
def hello(instance_id):
    logger.info("Hello, world!")
    instance = VideoUpload.objects.get(id=instance_id)
    instance.adminVideo = None
    instance.save()
    


@shared_task
def convert_and_merge_videos(instance_id):
    instance = VideoUpload.objects.get(id=instance_id)
    
    video_admin_path = instance.adminVideo.path
    video_client_path = instance.clientVideo.path

    video_admin_mp4 = convert_to_mp4(video_admin_path)
    video_client_mp4 = convert_to_mp4(video_client_path)

    if video_admin_mp4 and video_client_mp4:
        output_path = os.path.join(os.path.dirname(video_admin_mp4), f"merged_{instance.id}_{int(time.time())}.mp4")
        merged_video_path = merge_videos(video_admin_mp4, video_client_mp4, output_path)
        if merged_video_path:
            instance.video.name = os.path.relpath(merged_video_path, settings.MEDIA_ROOT)
            instance.save()
        else:
            raise Exception("Failed to merge videos.")
    else:
        raise Exception("Video conversion failed.")

def convert_to_mp4(input_path):
    try:
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_{int(time.time())}.mp4"
        subprocess.run([
            "ffmpeg", "-y", "-i", input_path, "-c:v", "libx264", "-c:a", "aac", output_path
        ], check=True)
        return output_path
    except subprocess.CalledProcessError as e:
        raise Exception(f"An error occurred during conversion: {e}")

def merge_videos(video_path_1, video_path_2, output_path):
    try:
        clip1 = VideoFileClip(video_path_1)
        clip2 = VideoFileClip(video_path_2)
        if clip1.duration != clip2.duration:
            raise ValueError("The videos must be of the same duration to merge them side by side.")
        combined = clips_array([[clip1, clip2]])
        combined.write_videofile(output_path, codec="libx264", audio_codec="aac")
        return output_path
    except Exception as e:
        raise Exception(f"An error occurred while merging videos: {e}")







@shared_task
def generate_otp():
    try:
        random_number = random.randint(100000, 999999)
        user = User.objects.first()
        OPT.objects.create(otp=random_number,user=user)
        return random_number
    except Exception as e:
        print('error',e)
        return None
        