from rest_framework import serializers
from .models import CallLog, SmsLog

class CallLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallLog
        fields = ['number','call_type','datetime','duration']

class SmsLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmsLog
        fields = ['address','sms_type','datetime','message','Contacts']