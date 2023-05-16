import re
import os
import sys
import django
from datetime import datetime

# Set up Django's settings
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ArgusAPI.settings')
django.setup()

# Import the CallLog model from  app's models.py
from API.models import CallLog, Contacts

def import_call_logs():
    with open('call_log.txt', 'r') as file:
        content = file.read()

    pattern = r"#\d+\nNumber\t: (.*)\nName\t: (.*)\nDate\t: (.*)\nType\t: (.*)\nDuration: (\d+)"
    matches = re.findall(pattern, content)
    for match in matches:
        number, name, date_str, call_type, duration_str = match
        date = datetime.strptime(date_str, "%a %b %d %H:%M:%S %Z%z %Y")
        duration = int(duration_str)
        number_last_10 = number[-10:] 

        try:
            contact = Contacts.objects.filter(number__endswith=number_last_10).first()
            call_log = CallLog(
                number=number,
                call_type=call_type,
                datetime=date,
                duration=duration,
                contacts=contact
            )
        except Contacts.DoesNotExist:
            call_log = CallLog(
                number=number,
                call_type=call_type,
                datetime=date,
                duration=duration,
                contacts=None
            )
        call_log.save()

# Run the import function
import_call_logs()
