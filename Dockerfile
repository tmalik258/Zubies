# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app

# Install the dependencies
RUN pip install -r requirements.txt && pip install --upgrade pip

# Copy the rest of the application code into the container
COPY . /app

# Expose the port the app runs on
EXPOSE 8002

# Set the environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Run the Django development server
CMD "sh -c python manage.py migrate && python manage.py runserver 0.0.0.0:8002"