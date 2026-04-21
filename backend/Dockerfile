# Source: NEW - Backend Dockerfile
# CORTEX MODIFICATION: Docker container for Cortex backend API

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create logs directory
RUN mkdir -p /var/log/cortex

# Run migrations and start server
ENV PYTHONUNBUFFERED=1
ENV LOG_LEVEL=DEBUG

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/docs || exit 1

# Start command
CMD ["sh", "-c", "alembic upgrade head && python -m uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4"]
