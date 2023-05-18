import requests

def send_image(filename):
    url = 'http://localhost:8000/api/face_reg/?format=json'  # Update with your actual endpoint URL
    files = {'image': open(filename, 'rb')}
    response = requests.post(url, files=files)
    
    if response.status_code == 200:
        found = response.json()
        print('Image uploaded successfully',found["found"])
    else:
        print('Error uploading image:',response.status_code)

# Usage: Call the function and pass the filename of the image you want to upload
send_image('D:\ID Proofs\Aachu\myphoto.jpg')
