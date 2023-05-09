import cv2
import face_recognition
import os
import pickle
from inputdata import *

set_of_encodings = []
for image in set_of_images:
    img = cv2.imread(image)
    face_locations = face_recognition.face_locations(img)
    face_encodings = face_recognition.face_encodings(img, face_locations)
    set_of_encodings.append(face_encodings)

with open('set_of_encodings.pkl', 'wb') as f:
    pickle.dump(set_of_encodings, f)
    