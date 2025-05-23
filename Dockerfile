# Use official slim Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /www/webchatbot

# Install system dependencies (minimize rebuilds)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install pip early and cache wheels
COPY req.txt .

RUN pip install -i https://pypi.org/simple --upgrade pip \
 && pip install --no-cache-dir -r req.txt


# Copy project files (after installing dependencies for better cache hit)
COPY . .

# Collect static if needed here (optional)
# RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Entrypoint (can be overridden by docker-compose)
CMD ["gunicorn", "webchatbot.wsgi:application", "--bind", "0.0.0.0:8000"]
