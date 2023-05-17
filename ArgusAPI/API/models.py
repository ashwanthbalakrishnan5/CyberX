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

    #adbstatus = models.DecimalField(max_digits=3, decimal_places=2)

class ADBStatus(models.Model):
    connec_status = models.CharField(max_length=255)
    photo_status = models.BooleanField(default=False)
    video_status = models.BooleanField(default=False)
    docs_status = models.BooleanField(default=False)
    device = models.OneToOneField(Device, on_delete=models.CASCADE, primary_key=True)


class DBStatus(models.Model):
    face_data_status = models.BooleanField(default=False)
    call_log_status = models.BooleanField(default=False)
    sms_log_status = models.BooleanField(default=False)
    contacts_status = models.BooleanField(default=False)
    photo_meta_status = models.BooleanField(default=False)
    video_meta_status = models.BooleanField(default=False)
    docs_meta_status = models.BooleanField(default=False)
    device = models.OneToOneField(Device, on_delete=models.CASCADE, primary_key=True)


class Contacts(models.Model):
    name = models.CharField(max_length=255)
    number = PhoneNumberField(default='+91')
    thumbnail = models.ImageField(upload_to=None,null=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE,null=True)


class CallLog(models.Model):
    INCOMING = 'Incoming'
    OUTGOING = 'Outgoing'
    MISSED = 'Missed'
    CALL_TYPE_CHOICES = [
        (INCOMING, 'Incoming'),
        (OUTGOING, 'Outgoing'),
        (MISSED ,'Missed')
    ]

    number = PhoneNumberField(default='+91')
    call_type = models.CharField(max_length=10, choices=CALL_TYPE_CHOICES)
    datetime = models.DateTimeField()
    duration = models.PositiveIntegerField()
    contacts = models.ForeignKey(
        Contacts, on_delete=models.SET_DEFAULT, default=None, null=True)


class SmsLog(models.Model):
    INCOMING = 'Incoming'
    OUTGOING = 'Outgoing'
    SMS_TYPE_CHOICES = [
        (INCOMING, 'Incoming'),
        (OUTGOING, 'Outgoing'),
    ]
    address = models.CharField(max_length=100)
    sms_type = models.CharField(max_length=10, choices=SMS_TYPE_CHOICES)
    datetime = models.DateTimeField()
    message = models.TextField()
    Contacts = models.ForeignKey(
        Contacts, on_delete=models.SET_DEFAULT, default=None, null=True)

class Photo(models.Model):
    photo_name = models.CharField(max_length=255)
    photo_path = models.CharField(max_length=1023)
    photo_type = models.CharField(max_length=255)
    photo_size = models.BigIntegerField()
    pixels = models.CharField(max_length=255)
    color_depth = models.CharField(max_length=255)
    image_comp = models.CharField(max_length=255)
    exif_date_time = models.DateTimeField()
    camera = models.CharField(max_length=255)
    exposure_time = models.DecimalField(max_digits=11,decimal_places=9)
    f_number = models.DecimalField(max_digits=4,decimal_places=2)
    iso_speed = models.IntegerField()
    focal_length = models.DecimalField(max_digits=7,decimal_places=5)
    gps = models.CharField(max_length=255)
    device = models.ForeignKey(Device, on_delete=models.CASCADE,null=True)

class Video(models.Model):
    video_name = models.CharField(max_length=255)
    video_path = models.CharField(max_length=1023)
    video_type = models.CharField(max_length=255)
    video_size = models.BigIntegerField()
    video_date_time = models.DateTimeField()
    duration = models.PositiveIntegerField()
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    fps = models.CharField(max_length=255)
    audio_codec = models.CharField(max_length=15)
    audio_channel = models.PositiveSmallIntegerField()
    audio_sample_rate = models.IntegerField()
    device = models.ForeignKey(Device, on_delete=models.CASCADE,null=True)

class Docs(models.Model):
    docs_name = models.CharField(max_length=255)
    docs_path = models.CharField(max_length=1023)
    docs_type = models.CharField(max_length=255)
    docs_size = models.BigIntegerField()
    docs_date_time = models.DateTimeField()
