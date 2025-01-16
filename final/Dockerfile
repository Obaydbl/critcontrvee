# Start from the Python base image
FROM python:3.11-slim

# Install required tools and add MySQL APT repository
RUN apt-get update && apt-get install -y \
    wget \
    lsb-release \
    gnupg \
    && wget https://dev.mysql.com/get/mysql-apt-config_0.8.26-1_all.deb \
    && dpkg -i mysql-apt-config_0.8.26-1_all.deb \
    && apt-get update

# Install MySQL development libraries and other dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    make \
    curl \
    git \
    build-essential \
    libmysqlclient-dev \
    libssl-dev \
    zlib1g-dev \
    && apt-get clean

# Upgrade pip, setuptools, and wheel
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Set the working directory
WORKDIR /app

# Copy requirements.txt and install Python dependencies
COPY requirements.txt /app/requirements.txt
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
