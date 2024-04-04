import os
import time
import requests

# Specify the folder and file name
folder_path = './compressedFiles'
file_name = 'compressed_files.tar.gz'
file_path = os.path.join(folder_path, file_name)
download_path ="./downloadedFiles"
# URL endpoints
upload_url = 'https://pythonassignment1-production.up.railway.app/upload'
download_url = 'https://pythonassignment1-production.up.railway.app/download'
downloaded_file_path = os.path.join(download_path, 'downloaded_' + file_name)
os.makedirs(download_path, exist_ok=True)

# Check if the file exists
if os.path.exists(file_path):
    # If the file exists, upload it
    with open(file_path, 'rb') as f:
        files = {'file': (file_name, f)}
        response = requests.post(upload_url, files=files)
        print("Upload response:", response.text)



    # Download the file
    response = requests.get(download_url)
    if response.status_code == 200:
        # Assuming the downloaded file should be saved with the same name
        # pdf_file_path = os.path.join(download_path, 'downloaded_' + file_name)
        with open('downloaded_' + file_name, 'wb') as f:
            f.write(response.content)
        print("File downloaded successfully.")
    else:
        print("Failed to download the file.")
else:
    print(f"The file {file_name} does not exist in {folder_path}.")
