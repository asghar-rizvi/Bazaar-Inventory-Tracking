# Base image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip uninstall -y gevent greenlet
RUN pip install --no-cache-dir gevent==20.9.0 greenlet==2.0.2
# Copy application code
COPY . .

# Environment variables (override in docker-compose)
ENV DB_URI=postgresql://postgres:asghar@db_master:5434/bazaar_stage3
ENV REPLICA_URI=postgresql://postgres:asghar@db_replica:5435/bazaar_stage3
ENV REDIS_URI=redis://redis:6379/0
ENV CELERY_BROKER=redis://redis:6379/0
ENV CELERY_BACKEND=redis://redis:6379/0
ENV SECRET_KEY=dev-key-123

# Expose ports
EXPOSE 5000

# Start script (uses Gunicorn for WSGI + Eventlet for Socket.IO)
CMD ["gunicorn", "--worker-class", "eventlet", "-w", "1", "-b", "0.0.0.0:5000", "app:app"]