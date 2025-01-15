# Use an official Python base image
FROM python:3.11-slim

# Install necessary dependencies including the CS50 library for C
RUN apt-get update && apt-get install -y \
    gcc \
    make \
    curl \
    libcs50-dev \
    && apt-get clean

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code
COPY . .

# Ensure the C binary is executable
RUN chmod +x ./c_program/my_binary

# Expose port 5000 for the Flask app
EXPOSE 5000

# Set the environment variable for Flask
ENV FLASK_APP=app.py

# Command to start Flask using Gunicorn for better performance in production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
