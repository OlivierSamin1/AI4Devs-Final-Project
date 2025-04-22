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
mkdir -p backend frontend data_privacy_vault email_processor document_processor ai_assistant nginx redis

# Create Docker configuration directory
mkdir -p docker

# Create volumes directory for persistent data
mkdir -p volumes/{redis,uploads,documents}
```

## Step 3: Set Up Docker Configuration Files

### Create Docker Compose File

Create a `docker-compose.yml` file in the docker directory:

```bash
touch docker/docker-compose.yml
```

Edit the file with the following configuration, which connects to the existing PostgreSQL database:

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
      - backend
    environment:
      - DJANGO_SETTINGS_MODULE=core.settings.development
      - DATABASE_URL=postgres://postgres:postgres@192.168.1.128:5432/personal_db
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
    # This enables communication with the external database on Raspberry Pi 3B
    driver_opts:
      com.docker.network.bridge.host_binding_ipv4: "0.0.0.0"
```

## Step 4: Verify Database Connection

Before proceeding, let's verify that we can connect to the existing PostgreSQL database on the Raspberry Pi 3B:

```bash
# Install PostgreSQL client tools if not already installed
sudo apt install postgresql-client -y

# Test connection to the database
psql -h 192.168.1.128 -U postgres -d personal_db
# Enter the PostgreSQL password when prompted
```

If the connection is successful, you'll see the PostgreSQL prompt. Type `\q` to exit.

If you encounter connection issues, verify that:
1. The Raspberry Pi 3B is powered on and connected to your network
2. The PostgreSQL container is running on the Raspberry Pi 3B
3. PostgreSQL is configured to accept remote connections
4. Any firewall on the Raspberry Pi 3B allows connections to port 5432

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

### Configure Django Database Settings

Create a Django settings module that connects to the existing PostgreSQL database:

```bash
mkdir -p core/settings
touch core/settings/__init__.py
touch core/settings/base.py
touch core/settings/development.py
touch core/settings/production.py
```

Add the following code to `core/settings/base.py`:

```python
import os
from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-default-dev-key')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'rest_framework',
    'corsheaders',
    'django_filters',
    'rest_framework_simplejwt',
    
    # Local apps
    'api',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# Database Configuration - connecting to existing PostgreSQL on Raspberry Pi 3B
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'personal_db'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'postgres'),
        'HOST': os.environ.get('DB_HOST', '192.168.1.128'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}

# JWT Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True  # Change this in production

# Celery settings
CELERY_BROKER_URL = os.environ.get('REDIS_URL', 'redis://redis:6379/0')
CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL', 'redis://redis:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
```

Add the following code to `core/settings/development.py`:

```python
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# CORS settings for development
CORS_ALLOW_ALL_ORIGINS = True
```

Add the following code to `core/settings/production.py`:

```python
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]']  # Add your domain or IP

# HTTPS settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# CORS settings for production
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "https://yourdomain.com",
]
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

## Step 9: Create Environment Files

Create environment files to store configuration values:

```bash
# Create .env file
touch .env
```

Add the following content to the .env file:

```
# Database configuration (connecting to existing PostgreSQL on Raspberry Pi 3B)
DB_NAME=personal_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=192.168.1.128
DB_PORT=5432

# Redis configuration
REDIS_HOST=redis
REDIS_PORT=6379

# Django configuration
DJANGO_SETTINGS_MODULE=core.settings.development
DJANGO_SECRET_KEY=development_secret_key_change_in_production

# API keys for service-to-service communication (if needed)
API_KEY_BACKEND_TO_DPV=backend_to_dpv_secret_key
```

## Step a: Verify Setup

Test your setup by running Docker Compose:

```bash
# Navigate to the docker directory
cd docker

# Start the Docker containers
docker-compose up -d

# Check if containers are running
docker-compose ps
```

You should see all containers running without any errors. If any containers fail to start, check the logs:

```bash
docker-compose logs
```

## Step b: Access the Applications

- Django backend: http://localhost:8000
- React frontend: http://localhost:3000
- Django admin: http://localhost:8000/admin
- Nginx: http://localhost:80

## Next Steps

Now that your development environment is set up and connected to the existing PostgreSQL database on Raspberry Pi 3B, proceed to [Container Infrastructure Setup](./02_container_infrastructure_setup.md) to configure all the Docker containers and services required for the Personal Database Assistant. 