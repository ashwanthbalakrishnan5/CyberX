# import cv2
# import face_recognition
# import os
# import pickle
# import json

# def predict(input_img):
#     input_face_locations = face_recognition.face_locations(input_img)
#     input_face_encodings = face_recognition.face_encodings(input_img, input_face_locations)
        
#     with open('media/facedata/set_of_encodings.pkl', 'rb') as f:
#         set_of_encodings = pickle.load(f)
        
#     results = []
#     for encodings in set_of_encodings:
#         for encoding in encodings:
#             result = face_recognition.compare_faces(input_face_encodings, encoding)
#             if True in result:
#                 results.append(True)
#                 break
#         else:
#             results.append(False)
        
#     found = []
#     for i in range(len(results)):
#         if results[i]:
#             found.append(set_of_images[i])
#     return found