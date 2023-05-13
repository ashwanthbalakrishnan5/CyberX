from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Device(models.Model):
    device_name = models.CharField(max_length=255)
    adbstatus = models.DecimalField(max_digits=3, decimal_places=2)
    last_update = models.DateTimeField(auto_now_add=True)
    face_data = models.BooleanField(default=False)
    call_log = models.BooleanField(default=False)
    sms_log = models.BooleanField(default=False)
    contacts_log = models.BooleanField(default=False)
    photo_meta = models.BooleanField(default=False)
    video_meta = models.BooleanField(default=False)
    docs_meta = models.BooleanField(default=False)


class Contacts(models.Model):
    name = models.CharField(max_length=255)
    number = PhoneNumberField()
    thumbnail = models.ImageField(upload_to=None)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)


class CallLog(models.Model):
    INCOMING = 'Incoming'
    OUTGOING = 'Outgoing'
    CALL_TYPE_CHOICES = [
        (INCOMING, 'Incoming'),
        (OUTGOING, 'Outgoing'),
    ]

    number = PhoneNumberField()
    call_type = models.CharField(max_length=10, choices=CALL_TYPE_CHOICES)
    datetime = models.DateTimeField()
    duration = models.PositiveIntegerField()
    contacts = models.ForeignKey(
        Contacts, on_delete=models.SET_DEFAULT, default="Unknown", null=True, blank=True)


class SmsLog(models.Model):
    INCOMING = 'Incoming'
    OUTGOING = 'Outgoing'
    SMS_TYPE_CHOICES = [
        (INCOMING, 'Incoming'),
        (OUTGOING, 'Outgoing'),
    ]
    address = models.CharField(max_length=100)
    number = PhoneNumberField()
    sms_type = models.CharField(max_length=10, choices=SMS_TYPE_CHOICES)
    datetime = models.DateTimeField()
    message = models.TextField()
    Contacts = models.ForeignKey(
        Contacts, on_delete=models.SET_DEFAULT, default=None, null=True, blank=True)
