import csv
import os
import tarfile
import shutil
import time
import subprocess
from flask import Flask, request, send_file
from threading import Timer
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Directories setup
UPLOAD_FOLDER = 'uploads'
MD_FOLDER = 'MD'
PDF_FOLDER = 'PDF'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MD_FOLDER, exist_ok=True)
os.makedirs(PDF_FOLDER, exist_ok=True)

# Path for the Markdown template, assumed to be in the root directory
MD_TEMPLATE_PATH = 'template.md'

def delayed_cleanup():
    try:
        os.remove('PDF.tar.gz')
        shutil.rmtree(PDF_FOLDER)
        shutil.rmtree(UPLOAD_FOLDER)
        os.makedirs(PDF_FOLDER, exist_ok=True)
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    except Exception as e:
        print(f"Cleanup error: {e}")

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file and file.filename.endswith('.tar.gz'):
        filename = secure_filename(file.filename)
        tar_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(tar_path)

        # Extract tar.gz file
        with tarfile.open(tar_path, 'r:gz') as tar:
            tar.extractall(UPLOAD_FOLDER)

        # Load the Markdown template
        with open(MD_TEMPLATE_PATH, 'r') as template_file:
            template = template_file.read()

        # Process each CSV file found
        for item in os.listdir(UPLOAD_FOLDER):
            if item.endswith('.csv'):
                csv_path = os.path.join(UPLOAD_FOLDER, item)
                with open(csv_path, 'r') as f:
                    reader = csv.reader(f)
                    next(reader)  # Skip header
                    for row in reader:
                        filled_template = template.replace('{{FirstName}}', row[0]).replace('{{LastName}}', row[1])
                        md_filename = f"{row[0].strip()}_{row[1].strip()}.md"
                        with open(os.path.join(MD_FOLDER, md_filename), 'w') as md_file:
                            md_file.write(filled_template)

        # Convert Markdown to PDF
        for md_file in os.listdir(MD_FOLDER):
            md_path = os.path.join(MD_FOLDER, md_file)
            with open(md_path, 'r') as file:
                md_content = file.read()
                pdf_path = os.path.join(PDF_FOLDER, md_file.replace(".md", ".pdf"))
                process = subprocess.run(['pandoc', '-o', pdf_path, '-f', 'markdown', '-t', 'pdf', md_path], capture_output=True, text=True)
                print("STDOUT:", process.stdout)
                print("STDERR:", process.stderr)

                if process.returncode != 0:
                    return f"Error converting {md_file} to PDF", 500

        # Compress PDF files into a new tar.gz
        pdf_tar_path = 'PDF.tar.gz'
        with tarfile.open(pdf_tar_path, 'w:gz') as tar:
            for pdf_file in os.listdir(PDF_FOLDER):
                pdf_path = os.path.join(PDF_FOLDER, pdf_file)
                tar.add(pdf_path, arcname=pdf_file)

        return 'Files processed and PDFs compressed', 200
    else:
        return 'Invalid file format', 400

@app.route('/download')
def download_file():
    pdf_tar_path = 'PDF.tar.gz'
    if not os.path.exists(pdf_tar_path):
        return 'PDF archive not found. Please try uploading and processing your files again.', 404

    # Attempt to send the file to the client
    response = send_file(pdf_tar_path, as_attachment=True)

    # Schedule cleanup to occur after a delay, ensuring the file has been sent
    Timer(10.0, delayed_cleanup).start()  # Adjust delay as needed

    return response

if __name__ == '__main__':
    # Use the PORT environment variable provided by Railway, defaulting to 5000 if not available
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
