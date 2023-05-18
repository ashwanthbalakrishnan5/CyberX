from rest_framework import serializers
from .models import *

class ContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = '__all__'
class CallLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallLog
        fields = ['number','call_type','datetime','duration','contacts']
    contacts = ContactsSerializer()

class SmsLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmsLog
        fields = ['address','sms_type','datetime','message','Contacts']

class DBStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = DBStatus
        fields = '__all__'

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'
