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
        fields = ['name','number','thumbnail','device']
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
