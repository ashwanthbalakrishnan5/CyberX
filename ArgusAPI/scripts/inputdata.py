import os

folder_path = "media/photos"

set_of_images = [os.path.join(folder_path, f) for f in os.listdir(
    folder_path) if f.endswith('.jpg') or f.endswith('.jpeg') or f.endswith('.png')]

