import csv
import os
import tarfile
import subprocess
from flask import Flask, request, send_file
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
                process = subprocess.run(['pandoc', '-o', pdf_path, '-f', 'markdown', '-t', 'pdf'], input=md_content, text=True)
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
    # Attempt to send the file to the client
    response = send_file('PDF.tar.gz', as_attachment=True)

    # Cleanup code: Delete the processed files
    try:
        # Delete generated PDF files
        for pdf_file in os.listdir(PDF_FOLDER):
            os.remove(os.path.join(PDF_FOLDER, pdf_file))

        # Delete Markdown files (optional, if you want to clean these up too)
        for md_file in os.listdir(MD_FOLDER):
            os.remove(os.path.join(MD_FOLDER, md_file))

        # Delete uploaded and extracted files (optional, careful with this)
        for uploaded_file in os.listdir(UPLOAD_FOLDER):
            file_path = os.path.join(UPLOAD_FOLDER, uploaded_file)
            if os.path.isfile(file_path):  # Check if it's a file and not a directory
                os.remove(file_path)

        # Finally, delete the compressed PDF file
        os.remove('PDF.tar.gz')

    except Exception as e:
        app.logger.error(f"Error during cleanup: {e}")
        # You might want to return a different response in case of cleanup failure
        # or just log the error, as done here.

    return response

if __name__ == '__main__':
    # Use the PORT environment variable provided by Railway, defaulting to 5000 if not available
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
