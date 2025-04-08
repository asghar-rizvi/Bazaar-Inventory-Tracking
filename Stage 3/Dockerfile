FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies including PostgreSQL development files
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev \
    postgresql-client \
    build-essential \
    && rm -rf /var/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip uninstall -y gevent greenlet && \
    pip install --no-cache-dir gevent==20.9.0 greenlet==2.0.2

# Copy application code
COPY . .

# Environment variables will be set in docker-compose
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Expose ports
EXPOSE 5000

# Start script (uses Gunicorn for WSGI + Eventlet for Socket.IO)
CMD ["gunicorn", "--worker-class", "eventlet", "-w", "1", "-b", "0.0.0.0:5000", "--timeout", "120", "app:app"]