import re
import os
import sys
import django
from datetime import datetime
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

    pattern = r"#\d+\nType\t: (.*)\nDate\t: (.*)\nAddress\t: (.*)\nStatus\t: (.*)\nMessage\t: (.*)"
    matches = re.findall(pattern, content)
    for match in matches:
        sms_type, date_str, address, status, message = match
        date = timezone.make_aware(datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S"))
        try:
            address_last_10 = address[-10:]
        except IndexError:
            address_last_10 = address
        try:
            contact = Contacts.objects.filter(number__endswith=address_last_10).first()
            sms_log = SmsLog(
                sms_type=sms_type,
                address=address,
                datetime=date,
                message=message,
                Contacts=contact
            )
        except Contacts.DoesNotExist:
            sms_log = SmsLog(
                sms_type=sms_type,
                address=address,
                datetime=date,
                message=message,
                Contacts=None
            )
        sms_log.save()

# Run the import function
# import_sms_logs()
