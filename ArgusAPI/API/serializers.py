from rest_framework import serializers
from .models import Contacts,CallLog,SmsLog,DBStatus,Photo,Video,ADBStatus,Device

class ADBStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ADBStatus
        fields = '__all__'

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'
class ContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = '__all__'
class CallLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallLog
        fields = '__all__'
    contacts = ContactsSerializer()

class SmsLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmsLog
        fields = '__all__'
    Contacts = ContactsSerializer()

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
