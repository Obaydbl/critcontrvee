# Start from the Python base image
FROM python:3.11-slim

# Install required system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    make \
    curl \
    git \
    build-essential \
    libmysqlclient-dev \
    default-libmysqlclient-dev \
    libssl-dev \
    zlib1g-dev \
    && apt-get clean

# Upgrade pip, setuptools, and wheel
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Set the working directory
WORKDIR /app

# Copy only requirements.txt
COPY requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt --verbose

# Copy the rest of the application code
COPY . /app

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose port 5000
EXPOSE 5000

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "app:app"]
