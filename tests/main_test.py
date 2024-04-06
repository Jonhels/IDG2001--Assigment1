import requests

# test if the server is running and can be connected to
def test_server_connection():
    response = requests.get("https://pythonfrontend-production.up.railway.app/")
    assert response.status_code == 200, "Could not connect to the server"

# test if the server can list files that is uploaded
def test_list_files():
    response = requests.get("https://pythonfrontend-production.up.railway.app/files/")
    assert response.status_code == 200, "Failed to list files"

# test if the server can list files that are ready to be downloaded
def test_download_files_list():
    response = requests.get("https://pythonfrontend-production.up.railway.app/downloadList/")
    assert response.status_code == 200, "Failed to list files to download"

# test if the server can upload files
import requests

def test_upload_endpoint_response():
    url = "https://pythonassignment1-production.up.railway.app/uploadfile/"
    response = requests.post(url)

    # Expected status code for the endpoint since no file is sent in the request
    expected_status_code = 404
    assert response.status_code == expected_status_code, f"Expected status code {expected_status_code}, but got {response.status_code}"
