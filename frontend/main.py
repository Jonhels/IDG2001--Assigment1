from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from typing import List
import os
import shutil
import tarfile
import subprocess

app = FastAPI()


UPLOAD_DIR = "uploadedFiles"
COMPRESSED_DIR = "compressedFiles"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(COMPRESSED_DIR, exist_ok=True)
compressed_file_path = os.path.join(COMPRESSED_DIR, 'compressed_files.tar.gz')


def compress_csv_files(folder_path, compressed_file_path):
    with tarfile.open(compressed_file_path, 'w:gz') as tar:
        for file in os.listdir(folder_path):
            if file.endswith('.csv'):
                tar.add(os.path.join(folder_path, file), arcname=file)

@app.post("/uploadfile/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    for file in files:
        # Ensure this checks for '.csv' files
        if file.filename and file.filename.endswith('.csv'):
            file_location = os.path.join(UPLOAD_DIR, str(file.filename))

            with open(file_location, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

    compress_csv_files(UPLOAD_DIR, compressed_file_path)

    subprocess.run(["python3", "upload.py"], check=True)

    return JSONResponse(content={"message": "CSV files uploaded and compressed successfully"}, status_code=200)

@app.get("/files/")
async def list_files():
    files = [f for f in os.listdir(UPLOAD_DIR) if os.path.isfile(os.path.join(UPLOAD_DIR, f))]
    return {"files": files}

@app.get("/downloadfile/")
async def download_latest_file():
    """
    Endpoint to download the latest file from the 'downloadedFiles' directory.
    """
    directory = "./downloadedFiles"
    try:
        # Find the latest file based on the last modification time
        latest_file = max([os.path.join(directory, f) for f in os.listdir(directory)], key=os.path.getmtime)
        return FileResponse(path=latest_file, filename=os.path.basename(latest_file), media_type='application/octet-stream')
    except ValueError:
        raise HTTPException(status_code=404, detail="No files found in the directory.")

app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import subprocess
    subprocess.run(["uvicorn", "main:app", "--reload"])
