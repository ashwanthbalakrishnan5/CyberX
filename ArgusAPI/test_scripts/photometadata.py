import os
import re
import sys
import django
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS

# Set up Django's settings
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ArgusAPI.settings')
django.setup()

from API.models import Photo

def PhotoMeta():
    folder_path = "D:\Programing\cyberx\ArgusAPI\media"
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".jpg") or file_name.endswith(".jpeg") or file_name.endswith(".png"):
            file_path = os.path.join(folder_path, file_name)
            img = Image.open(file_path)
            file_size = os.path.getsize(file_path)
            file_type = img.format
            date_created = os.path.getctime(file_path)
            date_modified = os.path.getmtime(file_path)
            pixels = img.size
            color_depth = img.mode
            image_compression = img.info.get("compression")
    
            exif_data = {}
            try:
                info = img._getexif()
                for tag, value in info.items():
                    decoded = TAGS.get(tag, tag)
                    exif_data[decoded] = value
                exif_date = exif_data.get("DateTimeOriginal")
                if exif_date:
                    exif_date = datetime.strptime(exif_date, "%Y:%m:%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
                exif_camera = exif_data.get("Make") + " " + exif_data.get("Model")
                #exif_camera_settings = exif_data.get("ExposureTime"), exif_data.get("FNumber"), exif_data.get("ISOSpeedRatings"), exif_data.get("FocalLength")
                exif_gps = exif_data.get("GPSInfo")
            except:
                exif_date,exif_camera,exif_gps = "","",""
            
            photo = Photo(
                photo_name = file_name,
                photo_path = file_path,
                photo_type = file_type,
                photo_size = file_size,
                pixels = pixels,
                color_depth = color_depth,
                image_comp = image_compression,
                exif_date_time = exif_date,
                camera = exif_camera,
                exposure_time = exif_data.get("ExposureTime"),
                f_number = exif_data.get("FNumber"),
                iso_speed = exif_data.get("ISOSpeedRatings"),
                focal_length = exif_data.get("FocalLength"),
                gps = exif_gps,
                device = None
            )
            photo.save()
    
        # print
        # print("File name:", file_name)
        # print("File path:", file_path)
        # print("File type:", file_type)
        # print("File size:", file_size, "bytes")
        # print("Date created:", datetime.fromtimestamp(date_created).strftime('%Y-%m-%d %H:%M:%S'))
        # print("Date last modified:", datetime.fromtimestamp(date_modified).strftime('%Y-%m-%d %H:%M:%S'))
        # print("Pixels:", pixels)
        # print("Color depth:", color_depth)
        # print("Image compression:", image_compression)
        # print("EXIF data:")
        # print("Date/time:", exif_date)
        # print("Camera:", exif_camera)
        # print("Camera settings:", exif_camera_settings)
        # print("GPS coordinates:", exif_gps)
        # print("-----------------------------------")
PhotoMeta()