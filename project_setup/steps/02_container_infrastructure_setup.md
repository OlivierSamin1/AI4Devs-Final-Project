# Container Infrastructure Setup

This guide covers the detailed setup of all Docker containers required for the Personal Database Assistant project, connecting to your existing PostgreSQL database on Raspberry Pi 3B.

## Container Architecture Overview

Our container infrastructure will connect to the existing database on Raspberry Pi 3B (at IP 192.168.1.128) while running application services locally:

1. **Database Server** (existing on Raspberry Pi 3B)
   - PostgreSQL database (already running at 192.168.1.128)
   - Data Privacy Vault (to be deployed as a container)

2. **Application Server** (local development environment, eventually Raspberry Pi 4)
   - Django Backend (REST API)
   - React Frontend
   - Celery Workers
   - Redis
   - Nginx

## Step 1: Create a Docker Network for External Database Communication

To enable communication with the existing PostgreSQL database on Raspberry Pi 3B, we'll create dedicated Docker networks:

```bash
# Create a network for the application components
docker network create --driver bridge app_network

# Create a network for communication with the external database
docker network create --driver bridge external_db_network
```

## Step 2: Update Docker Compose Configuration

Edit the `docker/docker-compose.yml` file to implement the network configuration and create distinct container groups:

```yaml
version: '3.8'

services:
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
      - DATABASE_URL=postgres://postgres:postgres@192.168.1.128:5432/personal_db
      - REDIS_URL=redis://redis:6379/0
      - DATA_PRIVACY_VAULT_URL=http://data_privacy_vault:8000
    volumes:
      - ../backend:/app
      - ../volumes/uploads:/app/uploads
    ports:
      - "8000:8000"
    networks:
      - app_network
      - external_db_network

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
      - app_network
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
      - app_network

  # Data Privacy Vault service
  data_privacy_vault:
    build:
      context: ../data_privacy_vault
      dockerfile: Dockerfile
    container_name: pda_vault
    restart: unless-stopped
    environment:
      - DB_HOST=192.168.1.128
      - DB_PORT=5432
      - DB_NAME=personal_db
      - DB_USER=postgres
      - DB_PASSWORD=postgres
    volumes:
      - ../data_privacy_vault:/app
    ports:
      - "8001:8000"
    networks:
      - external_db_network

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
      - app_network

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
    environment:
      - DATABASE_URL=postgres://postgres:postgres@192.168.1.128:5432/personal_db
    volumes:
      - ../document_processor:/app
      - ../volumes/documents:/app/documents
    networks:
      - app_network
      - external_db_network

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
    environment:
      - DATABASE_URL=postgres://postgres:postgres@192.168.1.128:5432/personal_db
    volumes:
      - ../email_processor:/app
    networks:
      - app_network
      - external_db_network

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
      - DATABASE_URL=postgres://postgres:postgres@192.168.1.128:5432/personal_db
    volumes:
      - ../ai_assistant:/app
    networks:
      - app_network
      - external_db_network

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
      - DATABASE_URL=postgres://postgres:postgres@192.168.1.128:5432/personal_db
      - REDIS_URL=redis://redis:6379/0
    volumes:
      - ../backend:/app
    networks:
      - app_network
      - external_db_network

networks:
  app_network:
    driver: bridge
  external_db_network:
    driver: bridge
    # Special configuration to allow external database access
    driver_opts:
      com.docker.network.bridge.host_binding_ipv4: "0.0.0.0"
```

## Step 3: Verify Database Connectivity

Before proceeding with the setup of other containers, verify that you can connect to the existing PostgreSQL database:

```bash
# Install PostgreSQL client (if not already installed)
sudo apt install postgresql-client

# Test connection to PostgreSQL on Raspberry Pi 3B
psql -h 192.168.1.128 -U postgres -d personal_db
```

When prompted, enter the password for the PostgreSQL user. If you can connect successfully, you'll see the PostgreSQL prompt. Exit the prompt by typing `\q`.

## Step 4: Create Service Directories and Files

Create the necessary directories and files for each service:

```bash
# Create directories for each service
mkdir -p backend frontend data_privacy_vault nginx document_processor email_processor ai_assistant
mkdir -p volumes/uploads volumes/documents volumes/redis nginx/{conf,ssl}
```

## Step 5: Configure Data Privacy Vault

The Data Privacy Vault will store sensitive user information in the existing PostgreSQL database but with enhanced encryption:

1. Create the `data_privacy_vault/Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

2. Create the `data_privacy_vault/requirements.txt`:

```
fastapi==0.95.1
uvicorn[standard]==0.22.0
pydantic==1.10.7
sqlalchemy==2.0.12
psycopg2-binary==2.9.6
python-dotenv==1.0.0
cryptography==40.0.2
```

3. Create the Data Privacy Vault application files:

`data_privacy_vault/main.py`:
```python
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, Integer, String, Text, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from cryptography.fernet import Fernet
import os
import base64
import hashlib
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Data Privacy Vault")

# Database configuration
DB_HOST = os.getenv("DB_HOST", "192.168.1.128")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "personal_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create a table specifically for storing encrypted data
metadata = MetaData()
encrypted_data = Table(
    "encrypted_data",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("data_type", String(50), index=True),
    Column("reference_id", String(100), index=True),
    Column("encrypted_value", Text),
    Column("encryption_key_id", String(50)),
)

engine = create_engine(DATABASE_URL)
metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Encryption key management (in a production environment, use a key management system)
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", Fernet.generate_key().decode())
fernet = Fernet(ENCRYPTION_KEY.encode() if isinstance(ENCRYPTION_KEY, str) else ENCRYPTION_KEY)

# Models
class SensitiveData(BaseModel):
    data_type: str
    reference_id: str
    value: str

class StoredDataResponse(BaseModel):
    id: int
    data_type: str
    reference_id: str

class RetrievedData(BaseModel):
    value: str

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API Endpoints
@app.post("/store", response_model=StoredDataResponse)
def store_sensitive_data(data: SensitiveData, db: Session = Depends(get_db)):
    encrypted_value = fernet.encrypt(data.value.encode()).decode()
    
    # Create a new record in the database
    query = encrypted_data.insert().values(
        data_type=data.data_type,
        reference_id=data.reference_id,
        encrypted_value=encrypted_value,
        encryption_key_id="default"  # In a production environment, track different keys
    )
    result = db.execute(query)
    db.commit()
    
    return {"id": result.inserted_primary_key[0], "data_type": data.data_type, "reference_id": data.reference_id}

@app.get("/retrieve/{data_type}/{reference_id}", response_model=RetrievedData)
def retrieve_sensitive_data(data_type: str, reference_id: str, db: Session = Depends(get_db)):
    # Query the database for the encrypted data
    query = encrypted_data.select().where(
        encrypted_data.c.data_type == data_type,
        encrypted_data.c.reference_id == reference_id
    )
    result = db.execute(query).first()
    
    if not result:
        raise HTTPException(status_code=404, detail="Data not found")
    
    # Decrypt the data
    decrypted_value = fernet.decrypt(result.encrypted_value.encode()).decode()
    
    return {"value": decrypted_value}

@app.delete("/delete/{data_type}/{reference_id}")
def delete_sensitive_data(data_type: str, reference_id: str, db: Session = Depends(get_db)):
    # Delete the record from the database
    query = encrypted_data.delete().where(
        encrypted_data.c.data_type == data_type,
        encrypted_data.c.reference_id == reference_id
    )
    result = db.execute(query)
    db.commit()
    
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Data not found")
    
    return {"detail": "Data deleted successfully"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
```

## Step 6: Configure Nginx

1. Create the `nginx/Dockerfile`:

```dockerfile
FROM nginx:1.23-alpine

COPY conf/default.conf /etc/nginx/conf.d/default.conf

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]
```

2. Create the Nginx configuration file `nginx/conf/default.conf`:

```nginx
server {
    listen 80;
    server_name localhost;
    
    location / {
        root /usr/share/nginx/html;
        index index.html index.htm;
        try_files $uri $uri/ /index.html;
    }
    
    location /api {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /admin {
        proxy_pass http://backend:8000/admin;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Static files for the Django admin interface
    location /static/admin/ {
        proxy_pass http://backend:8000/static/admin/;
    }
    
    # Media files
    location /media/ {
        proxy_pass http://backend:8000/media/;
    }
}
```

## Step 7: Start the Infrastructure

With all the container configurations in place, start the infrastructure:

```bash
# Navigate to the docker directory
cd docker

# Start all containers in detached mode
docker-compose up -d

# Check if all containers are running
docker-compose ps

# View logs for all containers
docker-compose logs

# View logs for a specific container
docker-compose logs backend
```

## Step 8: Test the Infrastructure

Verify that all components of the infrastructure are working correctly:

1. **Test the backend API**:
   ```bash
   curl http://localhost:8000/api/health-check/
   ```

2. **Test the frontend**:
   Open a web browser and navigate to `http://localhost:3000`

3. **Test the Nginx proxy**:
   ```bash
   curl http://localhost/api/health-check/
   ```

4. **Test the Data Privacy Vault**:
   ```bash
   curl http://localhost:8001/health
   ```

## Next Steps

With the container infrastructure successfully set up and connected to your existing PostgreSQL database on Raspberry Pi 3B, you're ready to proceed with developing the core application components:

1. Implement the Django backend API
2. Develop the React frontend
3. Configure the document and email processors
4. Set up the AI assistant functionality

Each of these components will be developed iteratively in upcoming implementation steps. 