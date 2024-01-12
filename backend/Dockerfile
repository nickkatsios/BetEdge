# Use a Python base image
FROM python:3.10

# Update package lists
RUN apt-get update

# Set environment variables
# -------------------------
# Setting PYTHONDONTWRITEBYTECODE to a non-empty value different from 0 ensures
#  that Python won’t try to write .pyc or .pyo files on the disk.
# Storing byte code on disk is used to compile python into byte code just upon the first 
# invocation of a program and its dependent libraries to save that step upon the following invocations.
# In a container the process runs just once, therefore setting this option makes sense.
ENV PYTHONDONTWRITEBYTECODE 1
# -------------------------
# Setting PYTHONUNBUFFERED to a non-empty value different from 0 ensures that the python output
# i.e. the stdout and stderr streams are sent straight to terminal (e.g. your container log) 
# without being first buffered and that you can see the output of your application (e.g. django logs) in real time.
# This also ensures that no partial output is held in a buffer somewhere and never written 
# in case the python application crashes.
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /backend

# Copy the requirements file to the working directory
COPY requirements.txt /backend/

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the Django project files to the working directory
COPY . /backend/

# Make migrations and create the database
RUN python manage.py makemigrations

# Expose the port the Django backend runs on
EXPOSE 8000
