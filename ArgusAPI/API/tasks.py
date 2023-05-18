from time import sleep
from celery import shared_task
from .models import Device ,DBStatus
from .extraction.Extractor import start_payload
# from .scripts.call_log import import_call_logs
from .scripts.photometadata import PhotoMeta
from .scripts.videometadata import VideoMeta
from .scripts.facedata import face_data

@shared_task
def start_extraction():
    pass
    status = start_payload()
    # if status.get("key") != "value":
    #     return "Error"

    db_status = DBStatus.objects.get(pk=1)
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
    


        


