# Container Infrastructure Setup

This guide covers the detailed setup of all Docker containers required for the Personal Database Assistant project. We'll configure each container with appropriate settings, networks, and volumes to simulate the final Raspberry Pi deployment architecture on your local machine.

## Container Architecture Overview

Our container infrastructure will simulate the two-device architecture that will eventually be deployed on the Raspberry Pi 3B and 4:

1. **Database Server** (simulating Raspberry Pi 3B)
   - PostgreSQL database
   - Data Privacy Vault

2. **Application Server** (simulating Raspberry Pi 4)
   - Django Backend (REST API)
   - React Frontend
   - Celery Workers
   - Redis
   - Nginx

## Step 1: Create a Docker Network for Inter-Pi Communication

To simulate the network separation between the two Raspberry Pis, we'll create dedicated Docker networks:

```bash
# Create a network for the "Pi 3B" (Database) components
docker network create --driver bridge pi3b_network

# Create a network for the "Pi 4" (Application) components
docker network create --driver bridge pi4_network

# Create a network for communication between the two "Pis"
docker network create --driver bridge inter_pi_network
```

## Step 2: Update Docker Compose Configuration

Edit the `docker/docker-compose.yml` file to implement the network separation and create distinct container groups:

```yaml
version: '3.8'

services:
  # Simulated Raspberry Pi 3B (Database Server) Services
  
  # Database service
  postgres:
    build:
      context: ../postgres
      dockerfile: Dockerfile
    container_name: pda_postgres
    restart: unless-stopped
    environment:
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_USER=postgres
      - POSTGRES_DB=personal_db
    volumes:
      - ../volumes/postgres:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    networks:
      - pi3b_network
      - inter_pi_network
  
  # Data Privacy Vault service
  data_privacy_vault:
    build:
      context: ../data_privacy_vault
      dockerfile: Dockerfile
    container_name: pda_vault
    restart: unless-stopped
    depends_on:
      - postgres
    volumes:
      - ../data_privacy_vault:/app
    ports:
      - "8001:8000"
    networks:
      - pi3b_network
      - inter_pi_network
  
  # Simulated Raspberry Pi 4 (Application Server) Services
  
  # Backend API service
  backend:
    build:
      context: ../backend
      dockerfile: Dockerfile
    container_name: pda_backend
    restart: unless-stopped
    depends_on:
      - redis
    environment:
      - DJANGO_SETTINGS_MODULE=core.settings.development
      - DATABASE_URL=postgres://postgres:postgres@postgres:5432/personal_db
      - REDIS_URL=redis://redis:6379/0
      - DATA_PRIVACY_VAULT_URL=http://data_privacy_vault:8000
    volumes:
      - ../backend:/app
      - ../volumes/uploads:/app/uploads
    ports:
      - "8000:8000"
    networks:
      - pi4_network
      - inter_pi_network

  # Frontend service
  frontend:
    build:
      context: ../frontend
      dockerfile: Dockerfile
    container_name: pda_frontend
    restart: unless-stopped
    volumes:
      - ../frontend:/app
      - /app/node_modules
    ports:
      - "3000:3000"
    networks:
      - pi4_network
    depends_on:
      - backend

  # Redis service
  redis:
    image: redis:7
    container_name: pda_redis
    restart: unless-stopped
    volumes:
      - ../volumes/redis:/data
    ports:
      - "6379:6379"
    networks:
      - pi4_network

  # Nginx service
  nginx:
    build:
      context: ../nginx
      dockerfile: Dockerfile
    container_name: pda_nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ../nginx/conf:/etc/nginx/conf.d
      - ../nginx/ssl:/etc/nginx/ssl
      - ../frontend/build:/usr/share/nginx/html
    depends_on:
      - backend
      - frontend
    networks:
      - pi4_network

  # Document processing worker
  document_processor:
    build:
      context: ../document_processor
      dockerfile: Dockerfile
    container_name: pda_document_processor
    restart: unless-stopped
    depends_on:
      - redis
      - backend
    volumes:
      - ../document_processor:/app
      - ../volumes/documents:/app/documents
    networks:
      - pi4_network
      - inter_pi_network

  # Email processing worker
  email_processor:
    build:
      context: ../email_processor
      dockerfile: Dockerfile
    container_name: pda_email_processor
    restart: unless-stopped
    depends_on:
      - redis
      - backend
    volumes:
      - ../email_processor:/app
    networks:
      - pi4_network
      - inter_pi_network

  # AI assistant worker
  ai_assistant:
    build:
      context: ../ai_assistant
      dockerfile: Dockerfile
    container_name: pda_ai_assistant
    restart: unless-stopped
    depends_on:
      - redis
      - backend
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ../ai_assistant:/app
    networks:
      - pi4_network
      - inter_pi_network

  # Celery worker for general tasks
  celery_worker:
    build:
      context: ../backend
      dockerfile: Dockerfile
    container_name: pda_celery_worker
    restart: unless-stopped
    command: celery -A core worker -l info
    depends_on:
      - redis
      - backend
    environment:
      - DJANGO_SETTINGS_MODULE=core.settings.development
      - DATABASE_URL=postgres://postgres:postgres@postgres:5432/personal_db
      - REDIS_URL=redis://redis:6379/0
    volumes:
      - ../backend:/app
    networks:
      - pi4_network
      - inter_pi_network

networks:
  pi3b_network:
    driver: bridge
  pi4_network:
    driver: bridge
  inter_pi_network:
    driver: bridge
```

## Step 3: Create Dockerfiles for Each Service

### 1. Data Privacy Vault

Create the Data Privacy Vault service directory structure and files:

```bash
# Create directory and navigate to it
mkdir -p data_privacy_vault
cd data_privacy_vault

# Create necessary files
touch Dockerfile requirements.txt
mkdir -p app
```

Create the Dockerfile:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc python3-dev libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy project
COPY . .

# Expose port
EXPOSE 8000

# Run server
CMD ["python", "app/main.py"]
```

Create requirements.txt:

```
fastapi==0.95.1
uvicorn==0.22.0
psycopg2-binary==2.9.6
pydantic==1.10.7
python-jose==3.3.0
passlib==1.7.4
python-multipart==0.0.6
cryptography==40.0.2
python-dotenv==1.0.0
```

Create the main application file:

```bash
touch app/main.py
```

Add the following initial content to app/main.py:

```python
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

app = FastAPI(title="Data Privacy Vault", 
              description="API for secure storage of sensitive personal data")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Token(BaseModel):
    token: str
    data_type: str

class SensitiveData(BaseModel):
    data: str
    data_type: str

@app.get("/")
async def root():
    return {"message": "Data Privacy Vault API"}

@app.post("/store")
async def store_sensitive_data(data: SensitiveData):
    # In a real implementation, this would:
    # 1. Encrypt the sensitive data
    # 2. Generate a token
    # 3. Store the encrypted data with the token
    # 4. Return only the token
    
    # This is a simplified placeholder
    token = f"token_{hash(data.data) % 10000}"
    return {"token": token}

@app.get("/retrieve/{token}")
async def retrieve_sensitive_data(token: str):
    # In a real implementation, this would:
    # 1. Validate the request
    # 2. Lookup the encrypted data using the token
    # 3. Decrypt the data
    # 4. Return the decrypted data
    
    # This is a simplified placeholder
    if not token.startswith("token_"):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Token not found"
        )
    
    # Mock data return
    return {"data": f"Sensitive data for {token}", "data_type": "mock"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
```

### 2. Document Processor

Create the Document Processor service directory structure and files:

```bash
# Navigate back to project root
cd ..

# Create directory and navigate to it
mkdir -p document_processor
cd document_processor

# Create necessary files
touch Dockerfile requirements.txt
mkdir -p app
```

Create the Dockerfile:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc python3-dev libpq-dev tesseract-ocr \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy project
COPY . .

# Create documents directory
RUN mkdir -p /app/documents

# Run worker
CMD ["python", "app/worker.py"]
```

Create requirements.txt:

```
celery==5.2.7
redis==4.5.4
pytesseract==0.3.10
Pillow==9.5.0
pdf2image==1.16.3
requests==2.28.2
python-dotenv==1.0.0
```

Create the worker application file:

```bash
touch app/worker.py
```

Add the following initial content to app/worker.py:

```python
import os
import time
from celery import Celery
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Celery
redis_url = os.getenv('REDIS_URL', 'redis://redis:6379/0')
app = Celery('document_processor', broker=redis_url)

@app.task(name='document_processor.process_document')
def process_document(document_path, document_type):
    """
    Process a document using OCR and extract relevant information.
    """
    logger.info(f"Processing document: {document_path} of type {document_type}")
    
    # Simulate processing time
    time.sleep(2)
    
    # In a real implementation, this would:
    # 1. Use OCR to extract text from the document
    # 2. Parse the text based on document type
    # 3. Extract structured data
    # 4. Send the data to the backend API
    
    logger.info(f"Document processed successfully: {document_path}")
    return {"status": "success", "message": f"Document {document_path} processed"}

if __name__ == '__main__':
    logger.info("Document Processor worker starting up...")
    app.start()
```

### 3. Email Processor

Create the Email Processor service directory structure and files:

```bash
# Navigate back to project root
cd ..

# Create directory and navigate to it
mkdir -p email_processor
cd email_processor

# Create necessary files
touch Dockerfile requirements.txt
mkdir -p app
```

Create the Dockerfile:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy project
COPY . .

# Run worker
CMD ["python", "app/worker.py"]
```

Create requirements.txt:

```
celery==5.2.7
redis==4.5.4
google-api-python-client==2.86.0
google-auth-httplib2==0.1.0
google-auth-oauthlib==1.0.0
requests==2.28.2
python-dotenv==1.0.0
```

Create the worker application file:

```bash
touch app/worker.py
```

Add the following initial content to app/worker.py:

```python
import os
import time
from celery import Celery
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Celery
redis_url = os.getenv('REDIS_URL', 'redis://redis:6379/0')
app = Celery('email_processor', broker=redis_url)

@app.task(name='email_processor.process_emails')
def process_emails(account_id, max_emails=10):
    """
    Process emails for the specified account.
    """
    logger.info(f"Processing emails for account: {account_id}, max: {max_emails}")
    
    # Simulate processing time
    time.sleep(2)
    
    # In a real implementation, this would:
    # 1. Connect to Gmail API using OAuth credentials
    # 2. Fetch recent emails
    # 3. Process email metadata and content
    # 4. Extract relevant information
    # 5. Send the data to the backend API
    
    logger.info(f"Emails processed successfully for account: {account_id}")
    return {"status": "success", "message": f"Processed {max_emails} emails for account {account_id}"}

if __name__ == '__main__':
    logger.info("Email Processor worker starting up...")
    app.start()
```

### 4. AI Assistant

Create the AI Assistant service directory structure and files:

```bash
# Navigate back to project root
cd ..

# Create directory and navigate to it
mkdir -p ai_assistant
cd ai_assistant

# Create necessary files
touch Dockerfile requirements.txt
mkdir -p app
```

Create the Dockerfile:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy project
COPY . .

# Run worker
CMD ["python", "app/worker.py"]
```

Create requirements.txt:

```
celery==5.2.7
redis==4.5.4
openai==0.27.6
requests==2.28.2
python-dotenv==1.0.0
```

Create the worker application file:

```bash
touch app/worker.py
```

Add the following initial content to app/worker.py:

```python
import os
import time
from celery import Celery
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Celery
redis_url = os.getenv('REDIS_URL', 'redis://redis:6379/0')
app = Celery('ai_assistant', broker=redis_url)

@app.task(name='ai_assistant.process_query')
def process_query(query, user_id, context=None):
    """
    Process a natural language query using AI.
    """
    logger.info(f"Processing query for user {user_id}: {query}")
    
    # Simulate processing time
    time.sleep(2)
    
    # In a real implementation, this would:
    # 1. Connect to OpenAI API
    # 2. Format the query with user context
    # 3. Get a response from the AI model
    # 4. Process and format the response
    # 5. Return the formatted response
    
    # Mockup response
    response = f"AI response to: {query}"
    
    logger.info(f"Query processed successfully for user {user_id}")
    return {"status": "success", "response": response}

if __name__ == '__main__':
    logger.info("AI Assistant worker starting up...")
    app.start()
```

### 5. Nginx Dockerfile

Create a Dockerfile for the Nginx service:

```bash
# Navigate back to project root
cd ..

# Navigate to nginx directory
cd nginx

# Create Dockerfile
touch Dockerfile
```

Add the following content to the Dockerfile:

```dockerfile
FROM nginx:alpine

# Remove default nginx config
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom nginx config
COPY conf/nginx.conf /etc/nginx/conf.d/

# Create directory for SSL certificates
RUN mkdir -p /etc/nginx/ssl

# Expose ports
EXPOSE 80 443

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
```

Create a directory for Nginx configuration:

```bash
mkdir -p conf
mv nginx.conf conf/
```

## Step 4: Create .env Files for Configuration

Create environment files for each service to store configuration values:

```bash
# Navigate back to project root
cd ..

# Create .env file for main project
touch .env
```

Add the following content to .env:

```
# OpenAI API key for AI assistant
OPENAI_API_KEY=your_openai_api_key

# Database configuration
DB_NAME=personal_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=postgres
DB_PORT=5432

# Redis configuration
REDIS_HOST=redis
REDIS_PORT=6379

# Data Privacy Vault configuration
DPV_URL=http://data_privacy_vault:8000

# API keys for service-to-service communication
API_KEY_BACKEND_TO_DPV=backend_to_dpv_secret_key
API_KEY_DPV_TO_BACKEND=dpv_to_backend_secret_key
```

## Step 5: Configure Docker Compose for Development and Production

Create separate Docker Compose files for development and production:

```bash
# Create docker-compose.dev.yml
touch docker/docker-compose.dev.yml

# Create docker-compose.prod.yml
touch docker/docker-compose.prod.yml
```

Add the following content to docker/docker-compose.dev.yml:

```yaml
version: '3.8'

# This extends the main docker-compose.yml file with development-specific settings
services:
  # Backend service overrides for development
  backend:
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - ../backend:/app
    environment:
      - DEBUG=True

  # Frontend service overrides for development
  frontend:
    command: npm start
    volumes:
      - ../frontend:/app
      - /app/node_modules
    environment:
      - NODE_ENV=development
      - REACT_APP_API_URL=http://localhost:8000/api
      - CHOKIDAR_USEPOLLING=true

  # Data Privacy Vault service overrides for development
  data_privacy_vault:
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    volumes:
      - ../data_privacy_vault:/app
    environment:
      - DEBUG=True

  # Document processor overrides for development
  document_processor:
    volumes:
      - ../document_processor:/app
    environment:
      - DEBUG=True

  # Email processor overrides for development
  email_processor:
    volumes:
      - ../email_processor:/app
    environment:
      - DEBUG=True

  # AI assistant overrides for development
  ai_assistant:
    volumes:
      - ../ai_assistant:/app
    environment:
      - DEBUG=True
```

Add the following content to docker/docker-compose.prod.yml:

```yaml
version: '3.8'

# This extends the main docker-compose.yml file with production-specific settings
services:
  # Backend service overrides for production
  backend:
    command: gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 3
    environment:
      - DEBUG=False
      - DJANGO_SETTINGS_MODULE=core.settings.production

  # Frontend service overrides for production
  frontend:
    command: nginx -g "daemon off;"
    volumes:
      - ../frontend/build:/usr/share/nginx/html
    environment:
      - NODE_ENV=production

  # Data Privacy Vault service overrides for production
  data_privacy_vault:
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 3
    environment:
      - DEBUG=False

  # Document processor overrides for production
  document_processor:
    environment:
      - DEBUG=False

  # Email processor overrides for production
  email_processor:
    environment:
      - DEBUG=False

  # AI assistant overrides for production
  ai_assistant:
    environment:
      - DEBUG=False

  # Nginx overrides for production
  nginx:
    volumes:
      - ../nginx/conf/nginx.prod.conf:/etc/nginx/conf.d/default.conf
      - ../frontend/build:/usr/share/nginx/html
      - ../backend/static:/usr/share/nginx/html/static
      - ../backend/media:/usr/share/nginx/html/media
```

## Step 6: Create Scripts for Container Management

Create a directory for utility scripts:

```bash
# Create scripts directory
mkdir -p scripts
```

### Create Start Script

```bash
touch scripts/start_dev.sh
chmod +x scripts/start_dev.sh
```

Add the following content to scripts/start_dev.sh:

```bash
#!/bin/bash

echo "Starting Personal Database Assistant in development mode..."

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Build and start the containers
cd docker
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

echo "Services started. Access the application at:"
echo "- Frontend: http://localhost:3000"
echo "- Backend API: http://localhost:8000/api"
echo "- Data Privacy Vault: http://localhost:8001"
echo "- Nginx: http://localhost:80"

echo "To view logs, run: docker-compose -f docker-compose.yml -f docker-compose.dev.yml logs -f"
```

### Create Stop Script

```bash
touch scripts/stop_dev.sh
chmod +x scripts/stop_dev.sh
```

Add the following content to scripts/stop_dev.sh:

```bash
#!/bin/bash

echo "Stopping Personal Database Assistant services..."

# Stop the containers
cd docker
docker-compose -f docker-compose.yml -f docker-compose.dev.yml down

echo "Services stopped."
```

### Create Build Script

```bash
touch scripts/build.sh
chmod +x scripts/build.sh
```

Add the following content to scripts/build.sh:

```bash
#!/bin/bash

echo "Building Personal Database Assistant containers..."

# Build the containers
cd docker
docker-compose -f docker-compose.yml build

echo "Build completed."
```

## Step 7: Verify Container Setup

Test your container setup by building and starting the services:

```bash
# Make scripts executable
chmod +x scripts/*.sh

# Build the containers
./scripts/build.sh

# Start the development services
./scripts/start_dev.sh
```

Verify that all containers are running correctly:

```bash
cd docker
docker-compose ps
```

You should see all containers running without any errors.

## Step A: Troubleshooting Common Issues

### Container Networking Issues

If containers cannot communicate with each other:

1. Verify the network configuration:
   ```bash
   docker network ls
   ```

2. Inspect the networks:
   ```bash
   docker network inspect pi3b_network
   docker network inspect pi4_network
   docker network inspect inter_pi_network
   ```

### Permission Issues with Volumes

If you encounter permission issues with mounted volumes:

```bash
# Fix permissions on volume directories
sudo chown -R $(id -u):$(id -g) volumes/
```

### Docker Compose Version Issues

If you encounter issues with Docker Compose syntax:

```bash
# Check Docker Compose version
docker-compose --version

# If using an older version, update it as shown in Setup guide
```

## Next Steps

Now that your container infrastructure is set up, you can proceed to [Backend API Development](./03_backend_api_development.md) to implement the core backend functionality for the Personal Database Assistant. 