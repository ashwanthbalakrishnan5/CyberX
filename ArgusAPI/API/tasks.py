from time import sleep
from celery import shared_task
from .models import Device ,DBStatus
from .extraction.Extractor import start_payload
from .scripts.call_log import import_call_logs
from .scripts.sms_log import import_sms_logs
from .scripts.contacts import import_contacts
from .scripts.photometadata import PhotoMeta
from .scripts.videometadata import VideoMeta
from .scripts.facedata import face_data

@shared_task
def PhotoMetaToDB():
    PhotoMeta()
    db_status.photo_meta_status = True
    db_status.save()

@shared_task
def VideoMetaToDB():
    VideoMeta()
    db_status.video_meta_status = True
    db_status.save()

@shared_task
def FaceToDB():
    face_data()
    db_status.face_data_status = False
    db_status.save()
    
@shared_task
def start_extraction():
    pass
    adb_handler = start_payload()
    # if status.get("key") != "value":
    #     return "Error"
    sleep(5)
    db_status = DBStatus.objects.create()

    import_contacts()
    db_status.contacts_status = True
    db_status.save()

    # Add callLog,sms,contacts to DB
    import_call_logs()
    db_status.call_log_status = True
    db_status.save()

    import_sms_logs()
    db_status.sms_log_status = True
    db_status.save()
    print("main data over")
    
    adb_handler.get_files()
    # # After Photos recieved
    # PhotoMeta()
    # db_status.photo_meta_status = True
    # db_status.save()
    PhotoMetaToDB.delay()
    # VideoMeta()
    # db_status.video_meta_status = True
    # db_status.save()
    VideoMetaToDB.delay()
    # #face_data()
    # db_status.face_data_status = False
    # db_status.save()
    FaceToDB.delay()


    


        


