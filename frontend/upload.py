import os
import time
import requests
import shutil

# Specify the folder paths
folder_path = './compressedFiles'  # For compressed files
download_path = "./downloadedFiles"  # For downloaded files
uploaded_path = "./uploadedFiles"  # Assuming this is your upload directory

file_name = 'compressed_files.tar.gz'
file_path = os.path.join(folder_path, file_name)
downloaded_file_path = os.path.join(download_path, 'downloaded_' + file_name)

# URL endpoints
#upload_url = 'https://pythonassignment1-production.up.railway.app/upload'
#download_url = 'https://pythonassignment1-production.up.railway.app/download'
upload_url = 'http://localhost:8089/upload'
download_url = 'http://localhost:8089/download'
# Ensure directories exist
os.makedirs(download_path, exist_ok=True)
os.makedirs(uploaded_path, exist_ok=True)  # Ensure the upload directory exists

# Check if the compressed file exists
if os.path.exists(file_path):
    # Upload it
    with open(file_path, 'rb') as f:
        files = {'file': (file_name, f)}
        response = requests.post(upload_url, files=files)
        print("Upload response:", response.text)

    # Wait for server processing
    time.sleep(5)

    # Download the processed file
    response = requests.get(download_url)
    if response.status_code == 200:
        with open(downloaded_file_path, 'wb') as f:
            f.write(response.content)
        print("File downloaded successfully.")

    else:
        print("Failed to download the file.")
else:
    print(f"The file {file_name} does not exist in {folder_path}.")
