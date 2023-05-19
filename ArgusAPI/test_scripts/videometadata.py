import os
from datetime import datetime
import ffmpeg

folder_path = "D:\Programing\cyberx\ArgusAPI\media"

for file_name in os.listdir(folder_path):
    if file_name.endswith(".mp4") or file_name.endswith(".mov") or file_name.endswith(".avi") or file_name.endswith(".mkv"):
        file_path = os.path.join(folder_path, file_name)

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
