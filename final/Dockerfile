
# Start from the Python base image
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    gcc \
    make \
    curl \
    git \
    build-essential \
    && apt-get clean

# Install libcs50 from the GitHub repository
RUN git clone https://github.com/cs50/libcs50.git /tmp/libcs50 && \
    cd /tmp/libcs50 && \
    make && \
    make install && \
    cd / && \
    rm -rf /tmp/libcs50

# Set the working directory
WORKDIR .

# Copy the requirements.txt (this ensures Docker uses cache unless requirements change)
COPY requirements.txt .

# Install dependencies (including Gunicorn and other Python libraries)
RUN pip install --no-cache-dir -r requirements.txt
# Set environment variable for Flask (optional but can be helpful)
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose port 5000 for the Flask app to be accessible
EXPOSE 5000

# Use gunicorn to serve the Flask app on port 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]