this file is just information

# URL endpoints backend

upload_url = 'https://pythonassignment1-production.up.railway.app/upload'
download_url = 'https://pythonassignment1-production.up.railway.app/download'

# URL endpoints frontend

# For local testing

upload_url = 'http://localhost:8089/upload'
download_url = 'http://localhost:8089/download'

But only if you have specified port 8089 inside docker when running the frontend container. If you have not specified the port, then you can use the default port 5000. I think its that one.
