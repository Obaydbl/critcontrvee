
# Start from the Python base image
FROM python:3.11-slim

# Install any system dependencies (e.g., cs50 library for C)
RUN apt-get update && apt-get install -y \
    gcc \
    make \
    curl \
    libcs50-dev \
    && apt-get clean

# Set the working directory
WORKDIR /app

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