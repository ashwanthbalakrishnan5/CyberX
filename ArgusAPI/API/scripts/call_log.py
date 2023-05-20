import re
import os
import sys
import django
from datetime import datetime,timedelta

# Set up Django's settings
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ArgusAPI.settings')
django.setup()

# Import the CallLog model from  app's models.py
from API.models import CallLog, Contacts
from ArgusAPI.settings import STORAGE_ROOT

def import_call_logs():
    with open(STORAGE_ROOT+'/data/calllog.txt', 'r',encoding='unicode-escape') as file:
        content = file.read()

    pattern = r"Row: \d+ number=(.*), date=(.*), type=(.*), duration=(.*), name=(.*)"
    matches = re.findall(pattern, content)
    for match in matches:
        number, date_milliseconds_str, call_type_num,duration_str ,name= match
        #date = datetime.strptime(date_str, "%a %b %d %H:%M:%S %Z%z %Y")
        duration = int(duration_str)
        number_last_10 = number[-10:] 
        call_type_key = int(call_type_num)
        call_types = ["check index","Incoming","Outgoing","Missed","VoiceMail","Rejected","Blocked","AnswerExternally"]
        if name == "":
            name = "Unknown"
        date_milliseconds = int(date_milliseconds_str)

        # Convert milliseconds to seconds
        date_seconds = date_milliseconds / 1000

        # Calculate the datetime object
        epoch = datetime(1970, 1, 1)
        date = epoch + timedelta(seconds=date_seconds)

        try:
            contact = Contacts.objects.filter(number__endswith=number_last_10).first()
            call_log = CallLog(
                number=number,
                call_type=call_types[call_type_key],
                datetime=date,
                duration=duration,
                name=name,
                contacts=contact
            )
        except Contacts.DoesNotExist:
            call_log = CallLog(
                number=number,
                call_type=call_types[call_type_key],
                datetime=date,
                duration=duration,
                name=name,
                contacts=None
            )
        call_log.save()

# Run the import function
#import_call_logs()
