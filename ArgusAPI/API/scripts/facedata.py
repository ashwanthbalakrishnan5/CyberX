import cv2
import face_recognition
import os
import pickle
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ArgusAPI.settings')
django.setup()

from ArgusAPI.settings import STORAGE_ROOT
def face_data():
    folder_path = STORAGE_ROOT+"/files"

    set_of_images = [os.path.join(folder_path, f) for f in os.listdir(
        folder_path) if f.endswith('.jpg') or f.endswith('.jpeg') or f.endswith('.png')]

    set_of_encodings = []
    for image in set_of_images:
        img = cv2.imread(image)
        face_locations = face_recognition.face_locations(img)
        face_encodings = face_recognition.face_encodings(img, face_locations)
        set_of_encodings.append(face_encodings)

    with open(STORAGE_ROOT+'/set_of_encodings.pkl', 'wb') as f:
        pickle.dump(set_of_encodings, f)
    with open(STORAGE_ROOT+'/set_of_images.pkl', 'wb') as f:
        pickle.dump(set_of_images, f)
    