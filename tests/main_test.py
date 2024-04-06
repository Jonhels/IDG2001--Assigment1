import requests

# test if the server is running and can be connected to
def test_server_connection():
    response = requests.get("https://pythonfrontend-production.up.railway.app/")
    assert response.status_code == 200, "Could not connect to the server"

def test_upload_files():
    files = {'file': open('tests/test_files/test.csv', 'rb')}
    response = requests.post("https://pythonfrontend-production.up.railway.app/upload", files=files)
    assert response.status_code == 200, "Failed to upload file(s)"
    
def test_list_files():
    response = requests.get("https://pythonfrontend-production.up.railway.app/files/")
    assert response.status_code == 200, "Failed to list files"
    
def test_download_files_list():
    response = requests.get("https://pythonfrontend-production.up.railway.app/downloadList/")
    assert response.status_code == 200, "Failed to list files to download"

def test_empty_file_upload():
    # Create an empty file
    with open('tests/test_files/empty.csv', 'w') as f:
        pass

    # Try to upload the empty file
    files = {'file': open('tests/test_files/empty.csv', 'rb')}
    response = requests.post("https://pythonfrontend-production.up.railway.app/uploadfile/", files=files)

    # Check that the server responded with an error message
    assert response.status_code == 422, "Server did not respond with an error message when trying to upload an empty file"
