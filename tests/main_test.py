import requests

# test if the server is running (this is my railway so it might not be online)
def test_server_connection():
    response = requests.get("https://oblig1-cloud-frontend-production.up.railway.app")
    assert response.status_code == 200, "Could not connect to the server"

def test_upload_files():
    files = {'file': open('tests/test_files/test.csv', 'rb')}
    response = requests.post("https://oblig1-cloud-frontend-production.up.railway.app/upload", files=files)
    assert response.status_code == 200, "Failed to upload file(s)"
    
def test_list_files():
    response = requests.get("https://oblig1-cloud-frontend-production.up.railway.app/files/")
    assert response.status_code == 200, "Failed to list files"
    
def test_download_files_list():
    response = requests.get("https://oblig1-cloud-frontend-production.up.railway.app/downloadList/")
    assert response.status_code == 200, "Failed to list files to download"
    