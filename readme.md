# IDG-2001--ASSIGNMENT1

# URL endpoints backend

upload_url = 'https://pythonassignment1-production.up.railway.app/upload'
download_url = 'https://pythonassignment1-production.up.railway.app/download'

# For local testing

upload_url = 'http://localhost:8089/upload'
download_url = 'http://localhost:8089/download'

But only if you have specified port 8089 inside docker when running the frontend container.
If you have not specified the port, then you can use the default port 5000. I think its that one.

## Description

This is a project for the course IDG2001 at NTNU Gjøvik. The project is a simple file upload and download service.
The project is split into two parts, the frontend and the backend. The frontend is a simple web page where you can upload a file and download a file.
The backend is a server that handles the file uploads and downloads. The backend is built using Flask and the frontend is built using HTML, CSS and JavaScript.

## Installation

To install the project, you need to clone the repository and install the dependencies. You can do this by running the following commands:

```bash
git clone
cd IDG2001--ASSIGNMENT1
pip install -r requirements.txt
```

The server should be hosted on railway.app here is my railway link https://pythonfrontend-production.up.railway.app/

Here is the backend if you want to test api endpoints https://pythonassignment1-production.up.railway.app

## Usage

To use the project you need to run the main.py file. This will start the server and you can access the endpoints through the browser or a tool like Postman. you also need to run backend that's where the file uploads are sent and processed before you can download the file again. Pls be patient largere files take longer to process.

We used docker to run the backend server. There is a docker file that you can build on your local machine. To build the docker image, run the following command:

```bash
docker build -t your-project-name .
```

## Testing

For this project we have used pytest. Run npm install pytest to install pytest. To run the tests, run pytest in the root directory of the project. This file is inside tests folder.

## Contributing

This project was created by Sebastian, Jon Helge and Mariam
