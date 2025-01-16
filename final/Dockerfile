# Start from the Python base image
FROM python:3.11-slim

# Install system dependencies first (these rarely change)
RUN apt-get update && apt-get install -y \
    gcc \
    make \
    curl \
    git \
    build-essential \
    && apt-get clean

# Clone and install libcs50 (this also doesn't change often)
RUN git clone https://github.com/cs50/libcs50.git /tmp/libcs50 && \
    cd /tmp/libcs50 && \
    make && \
    make install && \
    cd / && \
    rm -rf /tmp/libcs50

# Set the working directory
WORKDIR /

# Copy only requirements.txt first (helps Docker cache dependency installation)
COPY requirements.txt .

# Install Python dependencies (these change less often than code)
RUN pip install -r requirements.txt

# Copy the rest of your app's code
COPY . .

# Set environment variable for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose port 5000
EXPOSE 5000

CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:$PORT app:app"]
