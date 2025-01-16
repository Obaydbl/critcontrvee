# Start from the Python base image
FROM python:3.11-bullseye

# Upgrade pip, setuptools, and wheel for smooth installation of Python packages
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Set the working directory to the root directory
WORKDIR /

# Copy requirements.txt and install Python dependencies
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt --verbose

# Copy the rest of the application code to the root directory
COPY . /

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV PORT=5000

# Expose the port to match the default or runtime override
EXPOSE $PORT

# Run the application using `sh` to expand `$PORT` properly
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:$PORT app:app"]