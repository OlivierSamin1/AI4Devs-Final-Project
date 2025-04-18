# Development Environment Setup

This guide covers setting up your local development environment for the Personal Database Assistant project.

## Prerequisites

Before starting, ensure you have the following installed on your local machine:

- Git
- Docker Engine (version 20.10.0 or higher)
- Docker Compose (version 2.0.0 or higher)
- Python 3.9 or higher
- Node.js 18 or higher
- Visual Studio Code or your preferred IDE

## Step 1: Install Docker and Docker Compose

### For Ubuntu/Debian:

```bash
# Update package index
sudo apt update

# Install required packages
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common

# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# Add Docker repository
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

# Install Docker Engine
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.18.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Add your user to the docker group to run Docker without sudo
sudo usermod -aG docker $USER
```

After adding your user to the docker group, log out and log back in for the changes to take effect.

### Verify Installation:

```bash
# Check Docker version
docker --version

# Check Docker Compose version
docker-compose --version
```

## Step 2: Create Project Directory Structure

Create the project directory structure that will mirror what we'll use on the Raspberry Pi 4:

```bash
# Create project root directory
mkdir -p personal_db_assistant

# Create directories for each component
cd personal_db_assistant
mkdir -p backend frontend data_privacy_vault email_processor document_processor ai_assistant nginx redis postgres

# Create Docker configuration directory
mkdir -p docker

# Create volumes directory for persistent data
mkdir -p volumes/{postgres,redis,uploads,documents}
```

## Step 3: Set Up Docker Configuration Files

### Create Docker Compose File

Create a `docker-compose.yml` file in the docker directory:

```bash
touch docker/docker-compose.yml
```

Edit the file with the following configuration:

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
      - postgres
      - redis
    environment:
      - DJANGO_SETTINGS_MODULE=core.settings.development
      - DATABASE_URL=postgres://postgres:postgres@postgres:5432/personal_db
      - REDIS_URL=redis://redis:6379/0
    volumes:
      - ../backend:/app
      - ../volumes/uploads:/app/uploads
    ports:
      - "8000:8000"
    networks:
      - backend_network
      - frontend_network

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
      - frontend_network
    depends_on:
      - backend

  # Postgres database
  postgres:
    image: postgres:14
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
      - backend_network

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
      - backend_network

  # Nginx service
  nginx:
    image: nginx:alpine
    container_name: pda_nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ../nginx/nginx.conf:/etc/nginx/conf.d/default.conf
      - ../nginx/ssl:/etc/nginx/ssl
      - ../frontend/build:/usr/share/nginx/html
    depends_on:
      - backend
      - frontend
    networks:
      - frontend_network

  # Celery worker
  celery_worker:
    build:
      context: ../backend
      dockerfile: Dockerfile
    container_name: pda_celery_worker
    restart: unless-stopped
    command: celery -A core worker -l info
    depends_on:
      - redis
      - postgres
      - backend
    environment:
      - DJANGO_SETTINGS_MODULE=core.settings.development
      - DATABASE_URL=postgres://postgres:postgres@postgres:5432/personal_db
      - REDIS_URL=redis://redis:6379/0
    volumes:
      - ../backend:/app
    networks:
      - backend_network

networks:
  frontend_network:
    driver: bridge
  backend_network:
    driver: bridge
```

## Step 4: Set Up Database Simulation

For local development, we'll simulate the two-device architecture (Raspberry Pi 3B and 4) by using separate Docker containers.

### Create Database Service Dockerfile

```bash
touch postgres/Dockerfile
```

Edit the file with the following content:

```dockerfile
FROM postgres:14

# Add initialization scripts
COPY ./init-scripts/ /docker-entrypoint-initdb.d/

# Expose PostgreSQL port
EXPOSE 5432
```

Create a directory for initialization scripts:

```bash
mkdir -p postgres/init-scripts
touch postgres/init-scripts/01-create-tables.sql
```

Add basic table creation script:

```sql
-- Create basic schema for Personal Database Assistant
CREATE SCHEMA IF NOT EXISTS personal_data;

-- Create users table
CREATE TABLE IF NOT EXISTS personal_data.users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create assets table
CREATE TABLE IF NOT EXISTS personal_data.assets (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES personal_data.users(id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    asset_type VARCHAR(100) NOT NULL,
    value DECIMAL(15, 2),
    acquisition_date DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create financial_accounts table
CREATE TABLE IF NOT EXISTS personal_data.financial_accounts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES personal_data.users(id),
    account_name VARCHAR(255) NOT NULL,
    institution VARCHAR(255),
    account_type VARCHAR(100) NOT NULL,
    balance DECIMAL(15, 2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create transactions table
CREATE TABLE IF NOT EXISTS personal_data.transactions (
    id SERIAL PRIMARY KEY,
    account_id INTEGER REFERENCES personal_data.financial_accounts(id),
    transaction_date DATE NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    description TEXT,
    category VARCHAR(100),
    transaction_type VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create documents table
CREATE TABLE IF NOT EXISTS personal_data.documents (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES personal_data.users(id),
    title VARCHAR(255) NOT NULL,
    document_type VARCHAR(100) NOT NULL,
    file_path VARCHAR(255) NOT NULL,
    upload_date DATE NOT NULL,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create security schema for the Data Privacy Vault
CREATE SCHEMA IF NOT EXISTS security;

-- Create sensitive_data table in security schema
CREATE TABLE IF NOT EXISTS security.sensitive_data (
    id SERIAL PRIMARY KEY,
    token VARCHAR(255) UNIQUE NOT NULL,
    data_type VARCHAR(100) NOT NULL,
    encrypted_data BYTEA NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create access_log table in security schema
CREATE TABLE IF NOT EXISTS security.access_log (
    id SERIAL PRIMARY KEY,
    token VARCHAR(255) NOT NULL,
    access_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER,
    purpose VARCHAR(100) NOT NULL,
    access_type VARCHAR(50) NOT NULL
);
```

## Step 5: Setup the Backend Django Project

Initialize a basic Django project in the backend directory:

```bash
# Navigate to the backend directory
cd backend

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
source venv/bin/activate  # On Windows, use: venv\Scripts\activate

# Install Django and other required packages
pip install django djangorestframework django-cors-headers psycopg2-binary python-dotenv celery redis

# Create a new Django project
django-admin startproject core .

# Create a basic app
python manage.py startapp api
```

Create a Dockerfile for the backend:

```bash
touch Dockerfile
```

Add the following content:

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

# Run Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

Create a requirements.txt file:

```bash
touch requirements.txt
```

Add the following content:

```
# Django and REST framework
django==4.2.0
djangorestframework==3.14.0
django-cors-headers==4.0.0

# Database
psycopg2-binary==2.9.6
python-dotenv==1.0.0

# Celery
celery==5.2.7
redis==4.5.4

# Authentication
djangorestframework-simplejwt==5.2.2

# Utilities
django-filter==23.2
Pillow==9.5.0
```

## Step 6: Setup the Frontend React Project

Initialize a React project in the frontend directory:

```bash
# Navigate to the frontend directory
cd ../frontend

# Create a new React app with TypeScript
npx create-react-app . --template typescript

# Install additional dependencies
npm install axios react-router-dom @mui/material @mui/icons-material @emotion/react @emotion/styled
```

Create a Dockerfile for the frontend:

```bash
touch Dockerfile
```

Add the following content:

```dockerfile
FROM node:18-alpine

WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy project files
COPY . .

# Start development server
CMD ["npm", "start"]
```

## Step 7: Setup Nginx Configuration

Create an Nginx configuration file:

```bash
# Navigate to the nginx directory
cd ../nginx
mkdir -p ssl
touch nginx.conf
```

Add the following content to nginx.conf:

```nginx
server {
    listen 80;
    listen [::]:80;
    server_name localhost;
    
    # Redirect HTTP to HTTPS in production
    # return 301 https://$host$request_uri;
    
    # For development, we'll use HTTP
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
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /static {
        alias /usr/share/nginx/html/static;
    }
    
    location /media {
        alias /usr/share/nginx/html/media;
    }
}

# HTTPS server - Uncomment for production
# server {
#     listen 443 ssl;
#     listen [::]:443 ssl;
#     server_name localhost;
#     
#     ssl_certificate /etc/nginx/ssl/nginx.crt;
#     ssl_certificate_key /etc/nginx/ssl/nginx.key;
#     
#     location / {
#         root /usr/share/nginx/html;
#         index index.html index.htm;
#         try_files $uri $uri/ /index.html;
#     }
#     
#     location /api {
#         proxy_pass http://backend:8000;
#         proxy_set_header Host $host;
#         proxy_set_header X-Real-IP $remote_addr;
#         proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
#         proxy_set_header X-Forwarded-Proto $scheme;
#     }
#     
#     location /admin {
#         proxy_pass http://backend:8000;
#         proxy_set_header Host $host;
#         proxy_set_header X-Real-IP $remote_addr;
#         proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
#         proxy_set_header X-Forwarded-Proto $scheme;
#     }
# }
```

## Step 8: Set Up Git Repository

Initialize a Git repository and create a .gitignore file:

```bash
# Navigate to the project root
cd ..

# Initialize Git repository
git init

# Create .gitignore file
touch .gitignore
```

Add the following content to .gitignore:

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg

# Django
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal
media

# React
node_modules/
.npm
.env.local
.env.development.local
.env.test.local
.env.production.local
npm-debug.log*
yarn-debug.log*
yarn-error.log*
/build

# Docker
volumes/

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS
.DS_Store
.AppleDouble
.LSOverride
Thumbs.db
ehthumbs.db
Desktop.ini
```

## Step 9: Verify Setup

Test your setup by running Docker Compose:

```bash
# Navigate to the docker directory
cd docker

# Start the Docker containers
docker-compose up -d

# Check if containers are running
docker-compose ps
```

You should see all containers running without any errors.

## Step 10: Access the Applications

- Django backend: http://localhost:8000
- React frontend: http://localhost:3000
- Django admin: http://localhost:8000/admin
- Nginx: http://localhost:80

## Next Steps

Now that your development environment is set up, you can proceed to [Container Infrastructure Setup](./02_container_infrastructure_setup.md) to configure all the Docker containers and services required for the Personal Database Assistant. 