# Troubleshooting Guide

This guide provides solutions for common issues you might encounter when installing, configuring, or using the Personal Asset Management System.

> **IMPORTANT COMPATIBILITY NOTICE**: This project is currently **only compatible with Raspberry Pi devices** (ARM architecture). Support for x86/x64 systems via QEMU emulation is under development.

## Table of Contents

1. [Installation Issues](#installation-issues)
2. [Database Connection Problems](#database-connection-problems)
3. [Docker-Related Issues](#docker-related-issues)
4. [Platform Compatibility Issues](#platform-compatibility-issues)
5. [Django Administration Issues](#django-administration-issues)
6. [File Upload Problems](#file-upload-problems)
7. [Performance Issues](#performance-issues)
8. [Raspberry Pi Specific Issues](#raspberry-pi-specific-issues)
9. [Data Migration Problems](#data-migration-problems)
10. [User Interface Issues](#user-interface-issues)
11. [Security and Access Issues](#security-and-access-issues)

## Installation Issues

### Package Installation Fails

**Problem**: `pip install` commands fail with dependency errors.

**Solutions**:

1. Update pip:
   ```bash
   pip install --upgrade pip
   ```

2. Install package dependencies:
   ```bash
   sudo apt-get install python3-dev libpq-dev build-essential
   ```

3. Try installing with isolated mode:
   ```bash
   pip install --no-cache-dir -r requirements.txt
   ```

### Virtual Environment Issues

**Problem**: Virtual environment activation doesn't work or commands fail inside it.

**Solutions**:

1. Recreate the virtual environment:
   ```bash
   rm -rf venv
   python -m venv venv
   source venv/bin/activate  # On Linux/macOS
   venv\Scripts\activate     # On Windows
   ```

2. Check Python version compatibility:
   ```bash
   python --version
   # Ensure the version is 3.9 or higher
   ```

## Database Connection Problems

### Cannot Connect to PostgreSQL

**Problem**: Django reports it cannot connect to the PostgreSQL database.

**Solutions**:

1. Check if PostgreSQL is running:
   ```bash
   sudo systemctl status postgresql
   ```

2. Verify database settings in `.env`:
   ```
   DB_NAME=assetdb
   DB_USER=assetuser
   DB_PASSWORD=your_password
   DB_HOST=localhost  # or db for Docker
   DB_PORT=5432
   ```

3. Test direct connection:
   ```bash
   psql -U assetuser -h localhost -d assetdb
   ```

4. Check PostgreSQL logs:
   ```bash
   sudo tail -n 50 /var/log/postgresql/postgresql-13-main.log  # adjust version as needed
   ```

### Migration Errors

**Problem**: Django migrations fail with errors.

**Solutions**:

1. Check migration history:
   ```bash
   python manage.py showmigrations
   ```

2. Reset problematic migrations (development only):
   ```bash
   python manage.py migrate app_name zero
   python manage.py migrate app_name
   ```

## Docker-Related Issues

> **Important Note**: The Docker deployment method described here is only compatible with ARM architecture (Raspberry Pi devices) and will not work on x86/x64 systems.

### Container Build Failures

**Problem**: Docker container fails to build.

**Solutions**:

1. Check Docker logs:
   ```bash
   docker-compose logs --tail=100
   ```

2. Rebuild without cache:
   ```bash
   docker-compose build --no-cache
   ```

3. Check Dockerfile for errors:
   ```bash
   docker-compose config
   ```

### Docker Image Issues

**Problem**: Issues with the Docker image or base image not found.

**Solutions**:

1. Verify you're using an ARM-based device (Raspberry Pi):
   ```bash
   uname -m
   ```
   Should return `armv7l`, `armv8`, or `aarch64`. If it returns `x86_64` or `i386`, this Docker image won't work on your system.

2. Verify the base image is available:
   ```bash
   docker images | grep api:20230622
   ```

3. If the base image is not found, pull and tag it correctly:
   ```bash
   # Pull the base image from Docker Hub (ARM architecture only)
   docker pull aipoweredcompany/nas_database:base_with_requirements

   # Tag the image with the required name and tag
   docker tag aipoweredcompany/nas_database:base_with_requirements api:20230622
   ```

4. Check Dockerfile configuration:
   ```Dockerfile
   FROM api:20230622
   COPY database .
   WORKDIR /home
   CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000 && python watch_directory.py
   ```

5. Use the correct compose file for your environment:
   ```bash
   # For local development on Raspberry Pi
   docker-compose -f api_local.yaml up -d
   
   # For Raspberry Pi deployment
   docker-compose -f api_RPI.yaml up -d
   ```

### Architecture Compatibility Issues

**Problem**: The Docker image fails to run due to architecture incompatibility.

**Solutions**:

1. Verify your system architecture:
   ```bash
   uname -m
   ```

2. If you're using an x86/x64 system (returns `x86_64` or `i386`), you cannot use the provided Docker image. Instead:
   - Use the [Manual Installation](#manual-installation) method
   - Create a custom Docker image for your architecture
   
3. Ensure you're using a Raspberry Pi 4 or newer for optimal performance

### Container Startup Issues

**Problem**: Containers start but the application is inaccessible.

**Solutions**:

1. Check container status:
   ```bash
   docker-compose ps
   ```

2. View running container logs:
   ```bash
   docker-compose logs -f web
   ```

3. Check network connectivity:
   ```bash
   docker network ls
   docker network inspect database_v2_default
   ```

### Volume Permission Issues

**Problem**: Docker reports permission errors with mounted volumes.

**Solutions**:

1. Check volume permissions:
   ```bash
   ls -la /path/to/media
   ```

2. Adjust permissions for media directory:
   ```bash
   sudo chown -R 1000:1000 /path/to/media
   ```

## Platform Compatibility Issues

### Running on Unsupported Architecture

**Problem**: Attempting to run the system on x86/x64 architecture (standard PCs) rather than on ARM (Raspberry Pi).

**Solutions**:

1. **Current Options**:
   - Use a physical Raspberry Pi device (Recommended)
   - Use the Manual Installation method on your x86/x64 system with reduced functionality
   
2. **Upcoming QEMU Solution** (Not yet available):
   ```bash
   # Future commands for QEMU-based emulation will be provided once the feature is implemented
   ```

3. **Checking Your Architecture**:
   ```bash
   uname -m
   ```
   - ARM architectures: `armv7l`, `armv8`, `aarch64` (Compatible)
   - x86/x64 architectures: `x86_64`, `i386`, `i686` (Currently Incompatible)

### Testing x86/x64 Compatibility

If you're a developer interested in helping with the upcoming QEMU emulation feature:

1. **Prerequisites**:
   - Experience with QEMU
   - Knowledge of cross-architecture emulation
   - Understanding of Docker and container technology

2. **Development Status**:
   The QEMU emulation feature is currently in development. Watch the project repository for updates or reach out to the development team if you'd like to contribute.

## Django Administration Issues

### Admin Interface Not Loading

**Problem**: Django admin interface shows errors or doesn't load.

**Solutions**:

1. Check for JavaScript console errors in your browser
2. Verify static files are collected:
   ```bash
   python manage.py collectstatic --noinput
   ```

3. Check Django logs for errors:
   ```bash
   python manage.py runserver --traceback
   ```

### Missing Model Admin

**Problem**: Models don't appear in the admin interface.

**Solutions**:

1. Verify model is registered in `admin.py`:
   ```python
   from django.contrib import admin
   from .models import YourModel
   
   admin.site.register(YourModel)
   ```

2. Check if app is included in `INSTALLED_APPS` in settings.py

3. Restart the Django server

## File Upload Problems

### File Upload Fails

**Problem**: Cannot upload files or files are not saved correctly.

**Solutions**:

1. Check directory permissions for the upload directory:
   ```bash
   ls -la media/
   ```

2. Verify the MEDIA_URL and MEDIA_ROOT settings in settings.py:
   ```python
   MEDIA_URL = '/media/'
   MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
   ```

3. Check file size limits:
   ```python
   # in settings.py
   DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB
   ```

### Uploaded Files Not Displaying

**Problem**: Files upload successfully but don't display in the system.

**Solutions**:

1. Check the file URL path in the HTML source
2. Verify media URL configuration in urls.py:
   ```python
   from django.conf import settings
   from django.conf.urls.static import static
   
   urlpatterns = [
       # existing patterns
   ]
   
   if settings.DEBUG:
       urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
   ```

3. Check file permissions in the media directory

## Performance Issues

### Slow Admin Interface

**Problem**: Django admin interface loads slowly.

**Solutions**:

1. Optimize database queries:
   ```python
   class YourModelAdmin(admin.ModelAdmin):
       list_select_related = ('related_model',)
   ```

2. Add database indexes for frequently queried fields:
   ```python
   class YourModel(models.Model):
       # Add index to frequently filtered fields
       class Meta:
           indexes = [
               models.Index(fields=['field_name']),
           ]
   ```

3. Implement database query caching

### Memory Usage Problems

**Problem**: Application uses excessive memory.

**Solutions**:

1. Check for memory leaks using tools like `memory_profiler`
2. Optimize Django settings:
   ```python
   # In settings.py
   DEBUG = False  # in production
   ```

3. Adjust database connection pooling parameters

## Raspberry Pi Specific Issues

### Performance on Raspberry Pi

**Problem**: System runs slowly on Raspberry Pi.

**Solutions**:

1. Use an external SSD instead of SD card:
   ```bash
   # Mount external drive
   sudo mkdir -p /mnt/ssd
   sudo mount /dev/sda1 /mnt/ssd
   
   # Move Docker data directory
   sudo systemctl stop docker
   sudo rsync -a /var/lib/docker/ /mnt/ssd/docker/
   sudo mv /var/lib/docker /var/lib/docker.old
   sudo ln -s /mnt/ssd/docker /var/lib/docker
   sudo systemctl start docker
   ```

2. Allocate more swap space:
   ```bash
   sudo dphys-swapfile swapoff
   sudo nano /etc/dphys-swapfile
   # Set CONF_SWAPSIZE=2048
   sudo dphys-swapfile setup
   sudo dphys-swapfile swapon
   ```

3. Optimize Docker container resource limits:
   ```yaml
   # In docker-compose.yml
   services:
     web:
       # ...
       deploy:
         resources:
           limits:
             cpus: '0.5'
             memory: 512M
   ```

### Overheating Issues

**Problem**: Raspberry Pi overheats and throttles.

**Solutions**:

1. Install cooling solution (heatsinks or fan)
2. Monitor temperature:
   ```bash
   vcgencmd measure_temp
   ```

3. Adjust CPU governor:
   ```bash
   sudo apt-get install cpufrequtils
   sudo cpufreq-set -g conservative
   ```

## Data Migration Problems

### Failed Migrations

**Problem**: Database migrations fail or corrupt data.

**Solutions**:

1. Backup the database before migrations:
   ```bash
   pg_dump -U assetuser -h localhost -d assetdb > backup.sql
   ```

2. Run migrations with verbosity for more information:
   ```bash
   python manage.py migrate --verbosity 2
   ```

3. For complex data transformations, use Django's data migrations:
   ```bash
   python manage.py makemigrations app_name --empty -n migrate_data
   ```

### Data Consistency Issues

**Problem**: Database contains inconsistent or corrupted data.

**Solutions**:

1. Run Django database validation:
   ```bash
   python manage.py validate
   ```

2. Use Django's database-level validation:
   ```python
   class YourModel(models.Model):
       class Meta:
           constraints = [
               models.CheckConstraint(
                   check=models.Q(field__gte=0),
                   name="field_non_negative"
               ),
           ]
   ```

3. Implement data integrity checks in a management command

## User Interface Issues

### Form Submission Errors

**Problem**: Forms fail to submit or return validation errors.

**Solutions**:

1. Check browser console for JavaScript errors
2. Verify CSRF token is present in forms:
   ```html
   <form method="post">
       {% csrf_token %}
       <!-- form fields -->
   </form>
   ```

3. Check Django form validation logic:
   ```python
   def clean(self):
       cleaned_data = super().clean()
       # Custom validation
       return cleaned_data
   ```

### Display Issues

**Problem**: Interface elements don't display correctly.

**Solutions**:

1. Clear browser cache or try in private/incognito mode
2. Check if all static files are loaded correctly
3. Verify HTML structure and CSS compatibility

## Security and Access Issues

### Login Problems

**Problem**: Unable to log in to the system.

**Solutions**:

1. Reset user password:
   ```bash
   python manage.py changepassword username
   ```

2. Check if the user is active in the database:
   ```python
   # In Django shell
   python manage.py shell
   from django.contrib.auth.models import User
   user = User.objects.get(username='username')
   user.is_active = True
   user.save()
   ```

3. Verify authentication backend configuration in settings.py

### Permission Issues

**Problem**: Users cannot access certain features despite being logged in.

**Solutions**:

1. Check user permissions in Django admin
2. Verify permission requirements in views:
   ```python
   from django.contrib.auth.decorators import permission_required
   
   @permission_required('app.view_model')
   def view_function(request):
       # function body
   ```

3. Add required permissions programmatically:
   ```python
   # In Django shell
   from django.contrib.auth.models import User, Permission
   user = User.objects.get(username='username')
   permission = Permission.objects.get(codename='view_model')
   user.user_permissions.add(permission)
   user.save()
   ```

## Reporting Issues

If you encounter an issue not covered by this guide, please submit a bug report with the following information:

1. Detailed description of the problem
2. Steps to reproduce the issue
3. Expected and actual results
4. System information (OS, browser, etc.)
5. Relevant error messages or logs

Submit bug reports via the project's issue tracker or to the system administrator. 