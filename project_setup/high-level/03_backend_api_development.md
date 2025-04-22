# Backend API Development

This guide covers the development of the Django REST Framework backend API for the Personal Database Assistant project.

## Overview

We'll build a Django REST Framework application with the following components:
- User authentication with JWT tokens
- Database models for financial data
- API endpoints for data access and manipulation
- Secure communication with the Data Privacy Vault
- Integration with Celery for background tasks

## Step 1: Set Up Django Project Structure

First, let's organize our Django project with a proper directory structure:

```bash
cd backend

# Create settings directory for multiple environments
mkdir -p core/settings
touch core/settings/__init__.py
touch core/settings/base.py
touch core/settings/development.py
touch core/settings/production.py

# Create apps directory for Django apps
mkdir -p apps
touch apps/__init__.py

# Create apps for different components
mkdir -p apps/users apps/finances apps/documents apps/api
touch apps/users/__init__.py apps/finances/__init__.py apps/documents/__init__.py apps/api/__init__.py
```

## Step 2: Configure Django Settings

Let's set up the base settings in `core/settings/base.py`:

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
    'apps.users',
    'apps.finances',
    'apps.documents',
    'apps.api',
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

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'personal_db'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'postgres'),
        'HOST': os.environ.get('DB_HOST', 'postgres'),
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

# Data Privacy Vault settings
DATA_PRIVACY_VAULT_URL = os.environ.get('DATA_PRIVACY_VAULT_URL', 'http://data_privacy_vault:8000')
API_KEY_BACKEND_TO_DPV = os.environ.get('API_KEY_BACKEND_TO_DPV', 'backend_to_dpv_secret_key')
```

Now let's create the development settings in `core/settings/development.py`:

```python
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# CORS settings for development
CORS_ALLOW_ALL_ORIGINS = True
```

And production settings in `core/settings/production.py`:

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

## Step 3: Define Database Models

Let's create the models for our Django apps. First, the User model:

```bash
# Create models file for users app
touch apps/users/models.py
```

Add the following code to `apps/users/models.py`:

```python
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Custom user model for the Personal Database Assistant.
    """
    email = models.EmailField(_('email address'), unique=True)
    
    # Fields that will be tokenized in the Data Privacy Vault
    phone_number_token = models.CharField(max_length=255, blank=True, null=True)
    address_token = models.CharField(max_length=255, blank=True, null=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email
```

Next, let's create the Financial models:

```bash
# Create models file for finances app
touch apps/finances/models.py
```

Add the following code to `apps/finances/models.py`:

```python
from django.db import models
from apps.users.models import User


class Asset(models.Model):
    """
    Model representing a user's asset (real estate, vehicle, etc.).
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assets')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    asset_type = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=15, decimal_places=2)
    acquisition_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.asset_type})"


class FinancialAccount(models.Model):
    """
    Model representing a financial account (bank account, investment account, etc.).
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='financial_accounts')
    account_name = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    account_type = models.CharField(max_length=100)
    
    # Account number will be tokenized in the Data Privacy Vault
    account_number_token = models.CharField(max_length=255)
    
    balance = models.DecimalField(max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.account_name} at {self.institution}"


class Transaction(models.Model):
    """
    Model representing a financial transaction.
    """
    account = models.ForeignKey(FinancialAccount, on_delete=models.CASCADE, related_name='transactions')
    transaction_date = models.DateField()
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.TextField()
    category = models.CharField(max_length=100, blank=True)
    transaction_type = models.CharField(max_length=50, choices=[
        ('DEBIT', 'Debit'),
        ('CREDIT', 'Credit'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.transaction_type}: {self.amount} on {self.transaction_date}"
```

Now, let's create the Document models:

```bash
# Create models file for documents app
touch apps/documents/models.py
```

Add the following code to `apps/documents/models.py`:

```python
from django.db import models
from apps.users.models import User


class Document(models.Model):
    """
    Model representing a user document (receipt, invoice, contract, etc.).
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=255)
    document_type = models.CharField(max_length=100)
    file = models.FileField(upload_to='documents/')
    upload_date = models.DateField(auto_now_add=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title


class ExtractedData(models.Model):
    """
    Model representing data extracted from a document using OCR.
    """
    document = models.OneToOneField(Document, on_delete=models.CASCADE, related_name='extracted_data')
    data = models.JSONField()
    extraction_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Data from {self.document.title}"
```

## Step 4: Create API Serializers

Let's create serializers for our models:

```bash
# Create serializers directory for API app
mkdir -p apps/api/serializers
touch apps/api/serializers/__init__.py
touch apps/api/serializers/user_serializers.py
touch apps/api/serializers/finance_serializers.py
touch apps/api/serializers/document_serializers.py
```

Add the following code to `apps/api/serializers/user_serializers.py`:

```python
from rest_framework import serializers
from apps.users.models import User
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'first_name', 'last_name')
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
```

Add the following code to `apps/api/serializers/finance_serializers.py`:

```python
from rest_framework import serializers
from apps.finances.models import Asset, FinancialAccount, Transaction


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ('id', 'user', 'name', 'description', 'asset_type', 'value', 
                  'acquisition_date', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id', 'account', 'transaction_date', 'amount', 'description', 
                  'category', 'transaction_type', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class FinancialAccountSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True, read_only=True)
    
    class Meta:
        model = FinancialAccount
        fields = ('id', 'user', 'account_name', 'institution', 'account_type', 
                  'account_number_token', 'balance', 'transactions', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
```

Add the following code to `apps/api/serializers/document_serializers.py`:

```python
from rest_framework import serializers
from apps.documents.models import Document, ExtractedData


class ExtractedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtractedData
        fields = ('id', 'document', 'data', 'extraction_date')
        read_only_fields = ('id', 'extraction_date')


class DocumentSerializer(serializers.ModelSerializer):
    extracted_data = ExtractedDataSerializer(read_only=True)
    
    class Meta:
        model = Document
        fields = ('id', 'user', 'title', 'document_type', 'file', 'upload_date', 
                  'metadata', 'extracted_data', 'created_at', 'updated_at')
        read_only_fields = ('id', 'upload_date', 'created_at', 'updated_at')
```

## Step 5: Create API Views

Now, let's create the API views:

```bash
# Create views directory for API app
mkdir -p apps/api/views
touch apps/api/views/__init__.py
touch apps/api/views/user_views.py
touch apps/api/views/finance_views.py
touch apps/api/views/document_views.py
```

Add the following code to `apps/api/views/user_views.py`:

```python
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from apps.users.models import User
from apps.api.serializers.user_serializers import UserSerializer, UserRegistrationSerializer


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegistrationSerializer


class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user
```

Add the following code to `apps/api/views/finance_views.py`:

```python
from rest_framework import viewsets
from apps.finances.models import Asset, FinancialAccount, Transaction
from apps.api.serializers.finance_serializers import (
    AssetSerializer, FinancialAccountSerializer, TransactionSerializer
)


class AssetViewSet(viewsets.ModelViewSet):
    serializer_class = AssetSerializer
    
    def get_queryset(self):
        return Asset.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FinancialAccountViewSet(viewsets.ModelViewSet):
    serializer_class = FinancialAccountSerializer
    
    def get_queryset(self):
        return FinancialAccount.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    
    def get_queryset(self):
        account_id = self.request.query_params.get('account_id')
        if account_id:
            return Transaction.objects.filter(
                account_id=account_id, 
                account__user=self.request.user
            )
        return Transaction.objects.filter(account__user=self.request.user)
```

Add the following code to `apps/api/views/document_views.py`:

```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.documents.models import Document
from apps.api.serializers.document_serializers import DocumentSerializer
from celery import current_app


class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    
    def get_queryset(self):
        return Document.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        document = serializer.save(user=self.request.user)
        # Trigger document processing task
        current_app.send_task(
            'document_processor.process_document',
            args=[document.file.path, document.document_type],
            kwargs={}
        )
    
    @action(detail=True, methods=['post'])
    def process(self, request, pk=None):
        document = self.get_object()
        # Trigger document processing task
        current_app.send_task(
            'document_processor.process_document',
            args=[document.file.path, document.document_type],
            kwargs={}
        )
        return Response({'status': 'processing'}, status=status.HTTP_202_ACCEPTED)
```

## Step 6: Configure URL Routes

Now, let's set up the URL routing:

```bash
# Create urls.py for API app
touch apps/api/urls.py
```

Add the following code to `apps/api/urls.py`:

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from apps.api.views.user_views import UserRegistrationView, UserDetailView
from apps.api.views.finance_views import AssetViewSet, FinancialAccountViewSet, TransactionViewSet
from apps.api.views.document_views import DocumentViewSet

# Create a router for ViewSets
router = DefaultRouter()
router.register(r'assets', AssetViewSet, basename='asset')
router.register(r'accounts', FinancialAccountViewSet, basename='account')
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'documents', DocumentViewSet, basename='document')

urlpatterns = [
    # Authentication endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User endpoints
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('user/', UserDetailView.as_view(), name='user_detail'),
    
    # Include router URLs
    path('', include(router.urls)),
]
```

Update the main project URLs in `core/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.api.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

## Step a: Configure Celery for Asynchronous Tasks

Let's set up Celery in the Django project:

```bash
# Create celery.py in the core package
touch core/celery.py
```

Add the following code to `core/celery.py`:

```python
import os
from celery import Celery

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.development')

app = Celery('personal_db_assistant')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
```

Update the `core/__init__.py` file to import the Celery app:

```python
from .celery import app as celery_app

__all__ = ('celery_app',)
```

## Step 8: Create Service for Data Privacy Vault Integration

Let's create a service to interact with the Data Privacy Vault:

```bash
# Create services directory
mkdir -p apps/api/services
touch apps/api/services/__init__.py
touch apps/api/services/privacy_vault_service.py
```

Add the following code to `apps/api/services/privacy_vault_service.py`:

```python
import requests
import logging
import os
from django.conf import settings

logger = logging.getLogger(__name__)

class PrivacyVaultService:
    """
    Service for interacting with the Data Privacy Vault.
    """
    def __init__(self):
        self.base_url = settings.DATA_PRIVACY_VAULT_URL
        self.api_key = settings.API_KEY_BACKEND_TO_DPV
    
    def _get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'ApiKey {self.api_key}'
        }
    
    def store_sensitive_data(self, data, data_type):
        """
        Store sensitive data in the vault and return a token.
        """
        try:
            response = requests.post(
                f"{self.base_url}/store",
                json={"data": data, "data_type": data_type},
                headers=self._get_headers()
            )
            response.raise_for_status()
            return response.json().get('token')
        except requests.exceptions.RequestException as e:
            logger.error(f"Error storing data in privacy vault: {str(e)}")
            return None
    
    def retrieve_sensitive_data(self, token):
        """
        Retrieve sensitive data from the vault using a token.
        """
        try:
            response = requests.get(
                f"{self.base_url}/retrieve/{token}",
                headers=self._get_headers()
            )
            response.raise_for_status()
            return response.json().get('data')
        except requests.exceptions.RequestException as e:
            logger.error(f"Error retrieving data from privacy vault: {str(e)}")
            return None


# Create a singleton instance
privacy_vault = PrivacyVaultService()
```

## Step 9: Create Middleware for Request Logging

Create a middleware for logging API requests:

```bash
# Create middleware directory
mkdir -p apps/api/middleware
touch apps/api/middleware/__init__.py
touch apps/api/middleware/request_logging_middleware.py
```

Add the following code to `apps/api/middleware/request_logging_middleware.py`:

```python
import logging
import time
import json
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('api.requests')

class RequestLoggingMiddleware(MiddlewareMixin):
    """
    Middleware for logging API requests.
    """
    def process_request(self, request):
        request.start_time = time.time()
    
    def process_response(self, request, response):
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            
            # Don't log media or static file requests
            if not request.path.startswith(('/media/', '/static/')):
                log_data = {
                    'method': request.method,
                    'path': request.path,
                    'status_code': response.status_code,
                    'duration': round(duration * 1000, 2),  # in milliseconds
                    'user': str(request.user) if request.user.is_authenticated else 'anonymous',
                }
                
                logger.info(json.dumps(log_data))
        
        return response
```

Add this middleware to the MIDDLEWARE list in `core/settings/base.py`:

```python
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.api.middleware.request_logging_middleware.RequestLoggingMiddleware',  # Add this line
]
```

## Step 10: Create Django Apps Configuration

Let's create the configuration files for each app:

```bash
# Create apps.py files for each app
touch apps/users/apps.py
touch apps/finances/apps.py
touch apps/documents/apps.py
touch apps/api/apps.py
```

Add the following code to `apps/users/apps.py`:

```python
from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'
```

Add similar configuration for the other apps.

## Step 11: Run Migrations and Create Admin

Now, let's run migrations to create the database tables:

```bash
python manage.py makemigrations
python manage.py migrate
```

Create a superuser for Django admin:

```bash
python manage.py createsuperuser
```

## Step 12: Test the API

Start the Django development server:

```bash
python manage.py runserver 0.0.0.0:8000
```

You can now test the API endpoints:

- Register a user: POST to http://localhost:8000/api/register/
- Get a JWT token: POST to http://localhost:8000/api/token/
- Get user details: GET to http://localhost:8000/api/user/
- Create a financial account: POST to http://localhost:8000/api/accounts/
- List accounts: GET to http://localhost:8000/api/accounts/
- Add transactions: POST to http://localhost:8000/api/transactions/
- Upload a document: POST to http://localhost:8000/api/documents/

## Next Steps

Now that your backend API is set up, you can proceed to [Frontend Development](./04_frontend_development.md) to implement the React frontend application for the Personal Database Assistant. 