import re
import os
import sys
import django

# Set up Django's settings
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ArgusAPI.settings')
django.setup()

# Import the desired model from app's models.py
from API.models import Contacts
from ArgusAPI.settings import STORAGE_ROOT


def import_contacts():
    with open(STORAGE_ROOT+'/storage/data/contacts.txt', 'r', encoding='utf-16') as file:
        content = file.read()

    pattern = r"Row: \d+ display_name=(.*), number=(.*), notes=(.*)"
    matches = re.findall(pattern, content)
    for match in matches:
        display_name, number, notes= match

        if '*' in number or '#' in number:
            continue  # Skip this entry

        # Remove spaces between numbers
        number = re.sub(r"\s+", "", number)

        contacts = Contacts(
            name=display_name,
            number=number,
        )
        contacts.save()

# Run the import function
# import_contacts()

# text = "≡ƒöÑ"
# unicode_code_points = [ord(char) for char in text]
# unicode_representation = "U+" + " ".join([f"{code_point:04X}" for code_point in unicode_code_points])

# print(unicode_representation)
