# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .
COPY models.py .
COPY templates ./templates
COPY static ./static

# Create directory for SQLite database
RUN mkdir -p /app/instance

# Expose port
EXPOSE 8080

# Set environment variables
ENV FLASK_APP=app.py
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

# Run with gunicorn
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 120 app:app
