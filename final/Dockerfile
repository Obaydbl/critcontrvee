
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

# Copy your application files
COPY . .

# Expose the Flask port
EXPOSE 5000

# Command to run Gunicorn (to serve your Flask app in production)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
