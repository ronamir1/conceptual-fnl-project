# Use an official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.9-slim


# Updating Ubuntu packages
RUN apt-get update && yes|apt-get upgrade

# Adding wget and bzip2
RUN  apt-get -y install build-essential cmake git
RUN  apt-get -y install libopenblas-dev liblapack-dev
RUN  apt-get -y install libx11-dev libgtk-3-dev

COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app

# Install production dependencies.
RUN pip install cmake flask dlib face-recognition face-recognition-models gunicorn opencv-python pyrebase5 urllib3[secure] httplib2shim


# Copy local code to the container image.
#WORKDIR /app
#COPY . .

# Service must listen to $PORT environment variable.
# This default value facilitates local development.
ENV PORT 8080

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 4 --timeout 0 app:app

# to deploy run -  gcloud builds submit --config backend-cloud-build.yaml . --timeout=2h --machine-type e2-highcpu-32