# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container to /backend/app
WORKDIR /backend/app

# Copy the current directory contents into the container at /backend/app
COPY requirements.txt /backend/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r /backend/requirements.txt && \
    apt-get update && \
    apt-get install -y pandoc texlive && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /backend/app
COPY ./app ./

# Make port 5000 available
EXPOSE 5000

# Define environment variable to specify the Flask app
ENV FLASK_APP=script.py

# Run Gunicorn when the container launches
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:$PORT --timeout 120 script:app"]

# If you want to run the app without using Gunicorn, you can use the following command
#CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--timeout", "120", "script:app"]
