import os
import re
import sys
import django
from datetime import datetime
import ffmpeg

# Set up Django's settings
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ArgusAPI.settings')
django.setup()

from API.models import Video


def VideoMeta():
    folder_path = "E:\Edu\Projects\CyberX\cyberx\ArgusAPI\media\images"
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".mp4") or file_name.endswith(".mov") or file_name.endswith(".avi") or file_name.endswith(".mkv"):
            file_path = os.path.join(folder_path, file_name)

             # Retrieve video thumbnail
            thumbnail_filename = f"{file_name}.jpg"
            thumbnail_path = os.path.join(folder_path, thumbnail_filename)
            ffmpeg.input(file_path).output(thumbnail_path, vframes=1).run()
    
            # video info
            probe = ffmpeg.probe(file_path)
            video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
            audio_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'audio'), None)
            file_size = os.path.getsize(file_path)
            file_type = video_stream.get("codec_name")
            date_created = os.path.getctime(file_path)
            date_modified = os.path.getmtime(file_path)
            duration = video_stream.get("duration")
            width = video_stream.get("width")
            height = video_stream.get("height")
            frame_rate = video_stream.get("avg_frame_rate")
            audio_codec = audio_stream.get("codec_name")
            audio_channels = audio_stream.get("channels")
            audio_sample_rate = audio_stream.get("sample_rate")
            
            video = Video(
                video_name = file_name,
                thumbnail_path = thumbnail_path,
                video_path = file_path,
                video_type = file_type,
                video_size = file_size,
                video_date_time = date_created,
                duration = duration,
                width = width,
                height = height,
                fps = frame_rate,
                audio_codec = audio_codec,
                audio_channel = audio_channels,
                audio_sample_rate = audio_sample_rate,
                device = None
            )
            # print
            # print("File name:", file_name)
            # print("File type:", file_type)
            # print("File size:", file_size, "bytes")
            # print("Date created:", datetime.fromtimestamp(date_created).strftime('%Y-%m-%d %H:%M:%S'))
            # print("Date last modified:", datetime.fromtimestamp(date_modified).strftime('%Y-%m-%d %H:%M:%S'))
            # print("Duration:", duration, "seconds")
            # print("Resolution:", width, "x", height)
            # print("Frame rate:", frame_rate, "fps")
            # print("Audio codec:", audio_codec)
            # print("Audio channels:", audio_channels)
            # print("Audio sample rate:", audio_sample_rate, "Hz")
            # print("-----------------------------------")
