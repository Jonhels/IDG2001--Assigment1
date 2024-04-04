# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container to /backend/app
WORKDIR /backend/app

# First, copy only the requirements.txt file to avoid cache invalidation
COPY requirements.txt /backend/requirements.txt

# Install any needed packages specified in requirements.txt
# Also, install pandoc and pdflatex (part of texlive) which are required by your application
RUN pip install --no-cache-dir -r /backend/requirements.txt && \
    apt-get update && \
    apt-get install -y pandoc texlive && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Now, copy the rest of your app
COPY ./app ./

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable to specify the Flask app
ENV FLASK_APP=script.py

# Run Gunicorn when the container launches
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:$PORT --timeout 120 script:app"]
