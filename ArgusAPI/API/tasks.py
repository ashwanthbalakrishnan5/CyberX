from time import sleep
from celery import shared_task
from .models import Device ,DBStatus
from .payload.Extractor import start_payload
#from .scripts.call_log import import_call_logs
from .scripts.photometadata import PhotoMeta
from .scripts.videometadata import VideoMeta
#from .scripts.facedata import face_data

@shared_task
def start_extraction():
    pass
    status = start_payload()
    if status.get("key") != "value":
        return "Error"
    device = Device.objects.create(
            device_name='Your Device Name',
            vnet_status='Your VNET Status',
            battery_level=0,
            android_version=0,
            device_model='Your Device Model',
            device_manufacturer='Your Device Manufacturer'
        )
    device.save()
    db_status = DBStatus.objects.get(device=device)
    #import_call_logs()

    # Add callLog,sms,contacts to DB
    db_status.call_log_status = True
    db_status.save()

    db_status.sms_log_status = True
    db_status.save()

    # After Photos recieved
    #PhotoMeta()
    db_status.photo_meta_status = True
    db_status.save()
    #VideoMeta()
    db_status.video_meta_status = True
    db_status.save()
    #face_data()
    db_status.face_data_status = True
    db_status.save()

    


        


