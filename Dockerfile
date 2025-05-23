# Use official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /www/webchatbot

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY req.txt .
RUN pip install --upgrade pip && pip install -r req.txt

# Copy project files
COPY . .

# Expose Django default port
EXPOSE 8000

# Default command (overridden in docker-compose)
CMD ["gunicorn", "webchatbot.wsgi:application", "--bind", "0.0.0.0:8000"]
