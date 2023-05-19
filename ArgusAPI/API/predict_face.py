import cv2
import face_recognition
import os
import pickle
import json
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ArgusAPI.settings')
django.setup()

from ArgusAPI.settings import STORAGE_ROOT

def predict(input_img):
    input_face_locations = face_recognition.face_locations(input_img)
    input_face_encodings = face_recognition.face_encodings(input_img, input_face_locations)
        
    with open(STORAGE_ROOT+'/set_of_encodings.pkl', 'rb') as f:
        set_of_encodings = pickle.load(f)
    with open(STORAGE_ROOT+'/set_of_images.pkl', 'rb') as f:
        set_of_images = pickle.load(f)
        
    results = []
    for encodings in set_of_encodings:
        for encoding in encodings:
            result = face_recognition.compare_faces(input_face_encodings, encoding)
            if True in result:
                results.append(True)
                break
        else:
            results.append(False)
        
    found = []
    for i in range(len(results)):
        if results[i]:
            found.append(set_of_images[i])
    return found