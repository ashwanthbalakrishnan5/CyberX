import os

folder_path = "E:\Edu\Projects\CyberX\Testing"

set_of_images = [os.path.join(folder_path, f) for f in os.listdir(
    folder_path) if f.endswith('.jpg') or f.endswith('.jpeg') or f.endswith('.png')]

input_image = "D:\ID Proofs\Aachu\myphoto.jpg"
