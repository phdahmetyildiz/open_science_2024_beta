# This file is being archived on 15.11.2026 and is not part of the new version.
# Use an official Python image as a base
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the application code
COPY . .

# Set the environment variables
ENV FLASK_APP=flaskserver.py
ENV GOOGLE_CLIENT_ID="15290909298-a7t7e7e0hngfmcr6lug01qruf3r3b1eh.apps.googleusercontent.com"

# Expose the port
EXPOSE 5000

# Run the command to start the development server
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
