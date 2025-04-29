FROM arm64v8/python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    procps \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY jarvis/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
# Ensure python-json-logger is installed for structured logging
RUN pip install --no-cache-dir python-json-logger>=2.0.7

# Copy project
COPY jarvis/ /app/

# Copy entrypoint script
COPY infrastructure/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Create static and media directories with proper permissions
RUN mkdir -p /app/static /app/media \
    && chmod 777 /app/static /app/media

# Create a non-root user
RUN useradd -m appuser
RUN chown -R appuser:appuser /app
USER appuser

# Set entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "jarvis.wsgi:application"] 
