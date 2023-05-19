import re
import os
import sys
import django
from datetime import datetime, timedelta
from django.utils import timezone

# Set up Django's settings
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ArgusAPI.settings')
django.setup()

# Import the CallLog model from  app's models.py
from API.models import SmsLog, Contacts
from ArgusAPI.settings import STORAGE_ROOT


def import_sms_logs():
    with open(STORAGE_ROOT+'/data/sms.txt', 'r',encoding='unicode-escape') as file:
        content = file.read()

    pattern = r"Row: \d+ address=(.*), body=(.*), type=(.*), status=(.*), date=(.*)"
    matches = re.findall(pattern, content)
    for match in matches:
        address, body, sms_type_num, status, date_milliseconds_str = match
        # date = timezone.make_aware(datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S"))
        sms_type_key = int(sms_type_num)
        sms_types = ["check Index","Incoming","Outgoing","","","","","",""]
        date_milliseconds = int(date_milliseconds_str)

        # Convert milliseconds to seconds
        date_seconds = date_milliseconds / 1000

        # Calculate the datetime object
        epoch = datetime(1970, 1, 1)
        date = epoch + timedelta(seconds=date_seconds)
        try:
            address_last_10 = address[-10:]
        except IndexError:
            address_last_10 = address
        try:
            contact = Contacts.objects.filter(number__endswith=address_last_10).first()
            sms_log = SmsLog(
                sms_type=sms_types[sms_type_key],
                address=address,
                datetime=date,
                message=body,
                Contacts=contact
            )
        except Contacts.DoesNotExist:
            sms_log = SmsLog(
                sms_type=sms_types[sms_type_key],
                address=address,
                datetime=date,
                message=body,
                Contacts=None
            )
        sms_log.save()

# Run the import function
# import_sms_logs()
