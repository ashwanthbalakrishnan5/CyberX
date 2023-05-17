import cv2
import face_recognition
import os
import pickle
import json
from inputdata import *

def upload_image(request):
    if request.method == 'POST':
        image_file = request.FILES['image']
        
        # Convert the uploaded image file into a numpy array
        image_data = image_file.read()
        nparr = np.frombuffer(image_data, np.uint8)
        input_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Process the image
        input_face_locations = face_recognition.face_locations(input_img)
        input_face_encodings = face_recognition.face_encodings(input_img, input_face_locations)
        
        with open('set_of_encodings.pkl', 'rb') as f:
            set_of_encodings = pickle.load(f)
        
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
        
        # Render the result or perform any other action
        return render(request, 'upload_success.html', {'found': found})
    else:
        return render(request, 'upload_form.html')
