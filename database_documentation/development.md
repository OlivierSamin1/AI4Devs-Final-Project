# Development Guide

This document provides comprehensive instructions for setting up a development environment and contributing to the Personal Asset Management System.

> **IMPORTANT COMPATIBILITY NOTICE**: This project is currently **only compatible with Raspberry Pi devices** (ARM architecture). Support for x86/x64 systems via QEMU emulation is under development.

## Table of Contents

1. [Development Environment Setup](#development-environment-setup)
2. [Project Structure](#project-structure)
3. [Docker Configuration](#docker-configuration)
4. [Development Workflow](#development-workflow)
5. [Coding Standards](#coding-standards)
6. [Testing](#testing)
7. [Database Migrations](#database-migrations)
8. [Adding New Features](#adding-new-features)
9. [QEMU Emulation Development](#qemu-emulation-development)
10. [Documentation](#documentation)
11. [Troubleshooting Development Issues](#troubleshooting-development-issues)

## Development Environment Setup

### Prerequisites

- Python 3.9 or newer
- PostgreSQL 13 or newer
- Git
- Docker and Docker Compose (optional, for containerized development)

### Local Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/database_v2.git
   cd database_v2
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements/development.txt
   ```

4. **Set up local PostgreSQL database**:
   ```bash
   # Create database
   createdb assetdb

   # Optional: create dedicated user
   createuser -P assetuser
   # Then grant permissions in PostgreSQL
   ```

5. **Configure environment variables**:
   ```bash
   cp .env.example .env.dev
   ```
   
   Edit `.env.dev` with your local settings:
   ```
   DEBUG=True
   SECRET_KEY=your_development_secret_key
   DB_NAME=assetdb
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=localhost
   DB_PORT=5432
   ALLOWED_HOSTS=localhost,127.0.0.1
   UPLOADED_FILE_PATH=media/
   ```

6. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

7. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```

8. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

### Docker Development Setup

For containerized development:

1. **Build and start containers**:
   ```bash
   docker-compose -f docker-compose.dev.yml up -d
   ```

2. **Run migrations**:
   ```bash
   docker-compose -f docker-compose.dev.yml exec web python manage.py migrate
   ```

3. **Create a superuser**:
   ```bash
   docker-compose -f docker-compose.dev.yml exec web python manage.py createsuperuser
   ```

## Project Structure

The project follows a modular Django architecture:

```
database_v2/
├── admin_app/              # Administrative app
│   ├── models/
│   │   ├── document.py     # Document model
│   │   └── files.py        # Base and administrative file models
├── financial/              # Financial management app
│   ├── models/
│   │   ├── bank.py         # Bank and account models
│   │   └── files.py        # Financial file models
├── health/                 # Health management app
│   ├── models/
│   │   ├── bill.py         # Health bill models
│   │   ├── product.py      # Health product models
│   │   └── symptom.py      # Symptom models
├── insurance/              # Insurance management app
│   ├── models/
│   │   ├── company.py      # Insurance company models
│   │   └── contract.py     # Insurance contract models
├── real_estate/            # Real estate management app
│   ├── models/
│   │   ├── asset.py        # Property asset models
│   │   ├── bills.py        # Property bill models
│   │   ├── copro_management.py # Co-property management
│   │   ├── hollidays_management.py # Holiday rental management
│   │   ├── mortgage.py     # Mortgage models
│   │   ├── renting_management.py # Rental management
│   │   ├── tenant.py       # Tenant models
│   │   └── utilities.py    # Utility contract models
├── tax/                    # Tax management app
│   ├── models/
│   │   ├── management.py   # Tax management models
│   │   └── tax.py          # Tax models
├── transportation/         # Transportation app
│   ├── models/
│   │   ├── asset.py        # Vehicle models
│   │   └── files.py        # Transportation file models
├── config/                 # Project configuration
│   ├── settings/
│   │   ├── base.py         # Base settings
│   │   ├── development.py  # Development settings
│   │   └── production.py   # Production settings
│   ├── urls.py             # Main URL routing
│   └── wsgi.py             # WSGI configuration
├── project_documentation/  # Project documentation
├── templates/              # HTML templates
├── static/                 # Static files
├── media/                  # User-uploaded content
├── manage.py               # Django management script
├── docker-compose.yml      # Production Docker configuration
├── docker-compose.dev.yml  # Development Docker configuration
├── Dockerfile              # Docker image definition
└── requirements/           # Python dependencies
    ├── base.txt            # Base requirements
    ├── development.txt     # Development requirements
    └── production.txt      # Production requirements
```

## Docker Configuration

> **Important Note**: The Docker configuration described below is only compatible with ARM architecture (Raspberry Pi devices) and will not work on x86/x64 systems. For x86/x64 development, use the [Local Setup](#local-setup) method until QEMU emulation support is implemented.

The project uses Docker for development and deployment. The main Dockerfile is defined as:

```Dockerfile
FROM api:20230622
COPY database .
WORKDIR /home
CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000 && python watch_directory.py
```

### Docker Image Setup

Before building the project containers, you need to pull and tag the base Docker image:

```bash
# Pull the base image from Docker Hub (ARM architecture only)
docker pull aipoweredcompany/nas_database:base_with_requirements

# Tag the image with the required name and tag
docker tag aipoweredcompany/nas_database:base_with_requirements api:20230622
```

### Architecture Compatibility

This Docker setup is specifically designed for:
- ARM-based processors (Raspberry Pi 4 or newer)
- Will not work on x86/x64 systems (standard PCs, Macs, or most servers)

To check your system architecture:
```bash
uname -m
```
- ARM architectures: `armv7l`, `armv8`, `aarch64`
- x86/x64 architectures: `x86_64`, `i386`, `i686` (incompatible with this Docker image)

### Docker Compose Configurations

Different Docker Compose configurations are available:
- `api_local.yaml`: For local development environments on Raspberry Pi
- `api_RPI.yaml`: For Raspberry Pi deployment
- `docker-compose.yml`: For standard production deployment on Raspberry Pi

### Working with Docker

To build and start the development environment:

```bash
docker-compose -f docker-compose.dev.yml up -d
```

To run migrations in a Docker container:

```bash
docker-compose -f docker-compose.dev.yml exec web python manage.py migrate
```

To create a superuser in a Docker container:

```bash
docker-compose -f docker-compose.dev.yml exec web python manage.py createsuperuser
```

## Development Workflow

### Branching Strategy

We follow a Git Flow-inspired branching strategy:

- `main`: Production-ready code
- `develop`: Integration branch for features
- `feature/feature-name`: Feature branches
- `bugfix/bug-name`: Bug fix branches
- `hotfix/fix-name`: Production hotfixes

### Development Process

1. **Create a feature branch**:
   ```bash
   git checkout develop
   git pull
   git checkout -b feature/your-feature-name
   ```

2. **Make and commit changes**:
   ```bash
   # Make changes to code
   git add .
   git commit -m "Descriptive commit message"
   ```

3. **Push branch to remote**:
   ```bash
   git push -u origin feature/your-feature-name
   ```

4. **Create a pull request** from your feature branch to `develop`.

5. **Code review and merge** once approved.

## Coding Standards

We follow Django and Python best practices:

### Python Style

- Follow PEP 8 style guidelines
- Use docstrings for all functions, classes, and modules
- Maximum line length of 100 characters

### Django Conventions

- Model names are singular (e.g., `Asset`, not `Assets`)
- App names are plural and lowercase (e.g., `real_estate`, not `real_estate_app`)
- Use Django's ORM features instead of raw SQL when possible
- Apply migrations before committing model changes

### Domain-Driven Design

- Organize code by domain (e.g., real estate, finance)
- Use rich domain models with behaviors
- Follow bounded context principles

### Code Formatting

Use `black` and `isort` for consistent formatting:

```bash
# Install formatting tools
pip install black isort

# Format Python code
black .
isort .
```

## Testing

We use Django's built-in testing framework with pytest:

### Setting Up Tests

1. **Install testing requirements**:
   ```bash
   pip install -r requirements/development.txt
   ```

2. **Create test files** in a `tests/` directory within each app:
   ```
   app_name/
   ├── tests/
   │   ├── __init__.py
   │   ├── test_models.py
   │   └── test_views.py
   ```

### Writing Tests

Follow the AAA (Arrange, Act, Assert) pattern:

```python
def test_asset_creation():
    # Arrange
    user = User.objects.create_user(username='testuser')
    
    # Act
    asset = Asset.objects.create(
        owner=user,
        nickname="Test Property",
        address="123 Test St",
        postal_code=12345
    )
    
    # Assert
    assert asset.nickname == "Test Property"
    assert asset.owner == user
```

### Running Tests

```bash
# Run all tests
python manage.py test

# Run tests for a specific app
python manage.py test app_name

# Run with pytest
pytest
```

## Database Migrations

Django automatically generates migrations based on model changes:

### Creating Migrations

After changing models:

```bash
python manage.py makemigrations
```

### Applying Migrations

```bash
python manage.py migrate
```

### Migration Best Practices

- Always review generated migrations before committing
- Create data migrations for complex data transformations
- Test migrations on a copy of production data before deploying

## Adding New Features

### Adding a New Model

1. Create the model in the appropriate app:
   ```python
   # example_app/models/new_model.py
   from django.db import models
   
   class NewModel(models.Model):
       name = models.CharField(max_length=100)
       description = models.TextField(blank=True, null=True)
       
       class Meta:
           verbose_name_plural = "New Models"
           
       def __str__(self):
           return self.name
   ```

2. Register the model in the app's admin:
   ```python
   # example_app/admin.py
   from django.contrib import admin
   from .models.new_model import NewModel
   
   @admin.register(NewModel)
   class NewModelAdmin(admin.ModelAdmin):
       list_display = ('name',)
       search_fields = ('name',)
   ```

3. Create and apply migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

### Adding a New App

1. Create the app:
   ```bash
   python manage.py startapp new_app
   ```

2. Add the app to `INSTALLED_APPS` in settings:
   ```python
   INSTALLED_APPS = [
       # existing apps...
       'new_app',
   ]
   ```

3. Create models, views, urls as needed.

4. Include the app's URLs in the main urls.py:
   ```python
   urlpatterns = [
       # existing patterns...
       path('new-app/', include('new_app.urls')),
   ]
   ```

## QEMU Emulation Development

### Overview

A major upcoming feature is support for running this project on x86/x64 CPU architectures via QEMU emulation of the ARM environment. This section provides guidance for developers interested in contributing to this feature.

### Requirements

- Strong understanding of QEMU and cross-architecture emulation
- Experience with Docker and containerization
- Knowledge of ARM architecture and Raspberry Pi systems
- Familiarity with system-level programming

### Development Approach

The goal is to create a transparent emulation layer that allows the ARM-based Docker image to run on x86/x64 systems. This will be accomplished through:

1. **QEMU User-Mode Emulation**: Using QEMU to emulate ARM binaries on x86/x64 hosts
2. **Docker Integration**: Creating a modified Docker environment that transparently handles architecture differences
3. **Performance Optimization**: Ensuring acceptable performance on standard PC hardware

### Getting Started

If you're interested in contributing to this feature:

1. Set up a development environment with QEMU installed:
   ```bash
   # For Ubuntu/Debian
   sudo apt update
   sudo apt install qemu qemu-user qemu-user-static binfmt-support
   
   # Register ARM binary format
   sudo docker run --rm --privileged multiarch/qemu-user-static --reset -p yes
   ```

2. Test basic ARM emulation:
   ```bash
   # Test if ARM binaries can be executed
   qemu-arm -version
   ```

3. Clone the development branch for QEMU integration:
   ```bash
   git clone -b feature/qemu-emulation https://github.com/yourusername/database_v2.git
   cd database_v2
   ```

4. Join the development discussion in the project's communication channels

### Current Status

The QEMU emulation feature is in early development. Specific contributions needed include:

- Docker configuration for cross-architecture support
- Performance benchmarking and optimization
- Compatibility testing of all system features
- Documentation for setup and use

## Documentation

### Code Documentation

- Use docstrings for all functions, classes, and modules
- Follow Google's Python style guide for docstrings

Example:
```python
def calculate_mortgage_payment(principal, rate, term):
    """Calculate the monthly mortgage payment.
    
    Args:
        principal (float): The loan amount
        rate (float): Annual interest rate (decimal)
        term (int): Loan term in years
        
    Returns:
        float: Monthly payment amount
    """
    monthly_rate = rate / 12
    term_months = term * 12
    
    if monthly_rate == 0:
        return principal / term_months
        
    return principal * (monthly_rate * (1 + monthly_rate) ** term_months) / ((1 + monthly_rate) ** term_months - 1)
```

### Project Documentation

- Update the project documentation when adding features
- Document API endpoints and parameters
- Keep the README and related docs current

## Troubleshooting Development Issues

### Common Issues

#### Database Migration Conflicts

If you encounter migration conflicts:

1. Reset migrations (development only):
   ```bash
   # Remove migration files (backup first!)
   find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
   
   # Recreate initial migration
   python manage.py makemigrations
   
   # Apply to fresh database
   python manage.py migrate
   ```

#### Environment Setup Problems

If your environment isn't working correctly:

1. Verify virtual environment is active
2. Check environment variables are set correctly
3. Confirm database connection settings

#### Docker Issues

For Docker-related problems:

1. Rebuild containers:
   ```bash
   docker-compose -f docker-compose.dev.yml down
   docker-compose -f docker-compose.dev.yml build --no-cache
   docker-compose -f docker-compose.dev.yml up -d
   ```

2. Check container logs:
   ```bash
   docker-compose -f docker-compose.dev.yml logs -f
   ```

### Getting Help

- Check the project's issue tracker
- Review Django documentation
- Ask questions in the project's communication channels 