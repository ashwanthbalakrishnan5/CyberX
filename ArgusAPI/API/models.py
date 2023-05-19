from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Device(models.Model):
    device_name = models.CharField(max_length=255)
    vnet_status = models.CharField(max_length=255)
    last_update = models.DateTimeField(auto_now_add=True)
    battery_level = models.PositiveSmallIntegerField()
    android_version = models.PositiveSmallIntegerField()
    device_model = models.CharField(max_length=255)
    device_manufacturer = models.CharField(max_length=255)
    screenshot = models.BooleanField(default=False)

    # adbstatus = models.DecimalField(max_digits=3, decimal_places=2)


class ADBStatus(models.Model):
    connec_status = models.CharField(
        max_length=255, default="No device connected")
    photo_status = models.BooleanField(default=False)
    video_status = models.BooleanField(default=False)
    docs_status = models.BooleanField(default=False)


class DBStatus(models.Model):
    face_data_status = models.BooleanField(default=False)
    call_log_status = models.BooleanField(default=False)
    sms_log_status = models.BooleanField(default=False)
    contacts_status = models.BooleanField(default=False)
    photo_meta_status = models.BooleanField(default=False)
    video_meta_status = models.BooleanField(default=False)
    docs_meta_status = models.BooleanField(default=False)
    # call_log_count = models.IntegerField(default=0)
    # sms_log_count = models.IntegerField(default=0)
    # contacts_log_count = models.IntegerField(default=0)
    # photo_count = models.IntegerField(default=0)
    # video_count = models.IntegerField(default=0)
    # docs_count = models.IntegerField(default=0)


class Contacts(models.Model):
    name = models.CharField(max_length=255)
    number = PhoneNumberField(default='+91')
    thumbnail = models.ImageField(upload_to=None, null=True)


class CallLog(models.Model):
    # INCOMING = 'Incoming'
    # OUTGOING = 'Outgoing'
    # MISSED = 'Missed'
    # CALL_TYPE_CHOICES = [
    #     (INCOMING, 'Incoming'),
    #     (OUTGOING, 'Outgoing'),
    #     (MISSED, 'Missed')
    # ]

    number = PhoneNumberField(default='+91')
    call_type = models.CharField(max_length=255)
    datetime = models.DateTimeField()
    duration = models.PositiveIntegerField()
    name = models.CharField(max_length=255,null=True,blank=True)
    # contacts = models.ForeignKey(
    #     Contacts, on_delete=models.SET_DEFAULT, default=None, null=True)


class SmsLog(models.Model):
    # INCOMING = 'Incoming'
    # OUTGOING = 'Outgoing'
    # SMS_TYPE_CHOICES = [
    #     (INCOMING, 'Incoming'),
    #     (OUTGOING, 'Outgoing'),
    # ]
    address = models.CharField(max_length=100)
    sms_type = models.CharField(max_length=100)
    datetime = models.DateTimeField()
    message = models.TextField()
    Contacts = models.ForeignKey(
        Contacts, on_delete=models.SET_DEFAULT, default=None, null=True)


class Photo(models.Model):
    photo_name = models.CharField(max_length=255)
    photo_path = models.CharField(max_length=1023)
    photo_type = models.CharField(max_length=255, null=True)
    photo_size = models.BigIntegerField(null=True)
    pixels = models.CharField(max_length=255, null=True)
    color_depth = models.CharField(max_length=255, null=True)
    image_comp = models.CharField(max_length=255, null=True)
    exif_date_time = models.DateTimeField(null=True)
    camera = models.CharField(max_length=255, null=True)
    exposure_time = models.CharField(max_length=255, null=True)
    f_number = models.CharField(max_length=255, null=True)
    iso_speed = models.IntegerField(null=True)
    focal_length = models.CharField(max_length=255, null=True)
    gps = models.CharField(max_length=255, null=True)


class Video(models.Model):
    video_name = models.CharField(max_length=255)
    video_path = models.CharField(max_length=1023)
    thumbnail_path = models.CharField(max_length=1023)
    video_type = models.CharField(max_length=255, null=True)
    video_size = models.BigIntegerField(null=True)
    video_date_time = models.DateTimeField(null=True)
    duration = models.PositiveIntegerField(null=True)
    width = models.PositiveIntegerField(null=True)
    height = models.PositiveIntegerField(null=True)
    fps = models.CharField(max_length=255, null=True)
    audio_codec = models.CharField(max_length=15, null=True)
    audio_channel = models.PositiveSmallIntegerField(null=True)
    audio_sample_rate = models.IntegerField(null=True)


class Docs(models.Model):
    docs_name = models.CharField(max_length=255)
    docs_path = models.CharField(max_length=1023)
    docs_type = models.CharField(max_length=255)
    docs_size = models.BigIntegerField()
    docs_date_time = models.DateTimeField()
