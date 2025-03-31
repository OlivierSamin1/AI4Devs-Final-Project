# Database Server Connection

This document outlines the steps to connect to the existing PostgreSQL database server on the Raspberry Pi 3B and create a simple API client to fetch the FuerteVentura property reservation data for February 2025.

## Prerequisites

- The Raspberry Pi 3B database server is already set up and running on your local network
- PostgreSQL is installed and configured on the Raspberry Pi 3B
- The database schema and February 2025 reservation data already exist

## Database Connection Information

Before proceeding, you need to gather the following information about the existing database:

1. Database server IP address (e.g., 192.168.2.10)
2. PostgreSQL port (default is 5432)
3. Database name
4. Username and password with read access to the database
5. Table names and schema for:
   - Asset table (containing the FuerteVentura property)
   - Reservation table (containing February 2025 bookings)
   - RentalPlatform table (if relevant)

If you don't have this information, you can obtain it from the administrator of the Raspberry Pi 3B database server.

## API Service Implementation

We'll implement a simple Django REST API service on the Raspberry Pi 4 to fetch and expose the existing data:

1. Install required packages:
   ```bash
   pip3 install django djangorestframework django-cors-headers psycopg2-binary
   ```

2. Create a new Django project:
   ```bash
   mkdir -p ~/db_api_service
   cd ~/db_api_service
   django-admin startproject db_api .
   ```

3. Create a new Django app:
   ```bash
   python3 manage.py startapp reservation_api
   ```

4. Edit the project settings:
   ```bash
   nano db_api/settings.py
   ```

5. Update the settings with the correct database connection information:
   ```python
   # Add to INSTALLED_APPS
   INSTALLED_APPS = [
       # ... existing apps
       'rest_framework',
       'corsheaders',
       'reservation_api',
   ]

   # Add to MIDDLEWARE (before CommonMiddleware)
   MIDDLEWARE = [
       # ... existing middleware
       'corsheaders.middleware.CorsMiddleware',
       # ... rest of middleware
   ]

   # Database configuration - update with your actual database info
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'your_database_name',  # Replace with actual database name
           'USER': 'your_database_user',  # Replace with actual username
           'PASSWORD': 'your_database_password',  # Replace with actual password
           'HOST': '192.168.2.10',  # Replace with actual IP address
           'PORT': '5432',
       }
   }

   # CORS settings
   CORS_ALLOW_ALL_ORIGINS = False
   CORS_ALLOWED_ORIGINS = [
       "http://192.168.1.10:8000",
       "https://192.168.1.10",
   ]

   # REST Framework settings
   REST_FRAMEWORK = {
       'DEFAULT_PERMISSION_CLASSES': [
           'rest_framework.permissions.IsAuthenticated',
       ],
       'DEFAULT_AUTHENTICATION_CLASSES': [
           'rest_framework.authentication.BasicAuthentication',
           'rest_framework.authentication.SessionAuthentication',
       ],
   }
   ```

6. Create models in reservation_api/models.py that match your existing database schema:
   ```bash
   nano reservation_api/models.py
   ```

7. Add the following code (adjust field names to match your existing schema):
   ```python
   from django.db import models

   class Asset(models.Model):
       # These fields should match your existing database schema
       # The field names and types may need to be adjusted
       nickname = models.CharField(max_length=100)
       address = models.CharField(max_length=255)
       postal_code = models.CharField(max_length=20, null=True, blank=True)
       city = models.CharField(max_length=100, null=True, blank=True)
       country = models.CharField(max_length=100, null=True, blank=True)
       buying_date = models.DateField(null=True, blank=True)
       is_rented = models.BooleanField(default=False)

       class Meta:
           # If your table has a different name, specify it here
           db_table = 'asset'
           managed = False  # Important: don't try to manage this table

       def __str__(self):
           return self.nickname

   class RentalPlatform(models.Model):
       # These fields should match your existing database schema
       name = models.CharField(max_length=50)
       website = models.CharField(max_length=255, null=True, blank=True)

       class Meta:
           db_table = 'rental_platform'
           managed = False  # Important: don't try to manage this table

       def __str__(self):
           return self.name

   class Reservation(models.Model):
       # These fields should match your existing database schema
       asset = models.ForeignKey(Asset, on_delete=models.DO_NOTHING)
       platform = models.ForeignKey(RentalPlatform, on_delete=models.DO_NOTHING)
       reservation_number = models.CharField(max_length=50, null=True, blank=True)
       entry_date = models.DateField()
       number_of_nights = models.IntegerField()
       end_date = models.DateField(null=True, blank=True)
       renting_person_full_name = models.CharField(max_length=100, null=True, blank=True)
       price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
       created_at = models.DateTimeField(auto_now_add=True)

       class Meta:
           db_table = 'reservation'
           managed = False  # Important: don't try to manage this table

       def __str__(self):
           return f"{self.asset.nickname} - {self.entry_date}"
   ```

8. Create serializers in reservation_api/serializers.py:
   ```bash
   nano reservation_api/serializers.py
   ```

9. Add the following code:
   ```python
   from rest_framework import serializers
   from .models import Asset, RentalPlatform, Reservation

   class AssetSerializer(serializers.ModelSerializer):
       class Meta:
           model = Asset
           fields = '__all__'

   class RentalPlatformSerializer(serializers.ModelSerializer):
       class Meta:
           model = RentalPlatform
           fields = '__all__'

   class ReservationSerializer(serializers.ModelSerializer):
       platform_name = serializers.ReadOnlyField(source='platform.name')
       asset_name = serializers.ReadOnlyField(source='asset.nickname')
       
       class Meta:
           model = Reservation
           fields = [
               'id', 'asset_id', 'asset_name', 'platform_id', 'platform_name',
               'reservation_number', 'entry_date', 'number_of_nights', 'end_date',
               'renting_person_full_name', 'price', 'created_at'
           ]
   ```

10. Create views in reservation_api/views.py:
    ```bash
    nano reservation_api/views.py
    ```

11. Add the following code:
    ```python
    from rest_framework import viewsets
    from rest_framework.decorators import api_view, permission_classes
    from rest_framework.response import Response
    from rest_framework.permissions import IsAuthenticated
    from django.db.models import Q
    from datetime import datetime
    from .models import Asset, RentalPlatform, Reservation
    from .serializers import AssetSerializer, RentalPlatformSerializer, ReservationSerializer

    class AssetViewSet(viewsets.ReadOnlyModelViewSet):
        queryset = Asset.objects.all()
        serializer_class = AssetSerializer

    class RentalPlatformViewSet(viewsets.ReadOnlyModelViewSet):
        queryset = RentalPlatform.objects.all()
        serializer_class = RentalPlatformSerializer

    class ReservationViewSet(viewsets.ReadOnlyModelViewSet):
        queryset = Reservation.objects.all()
        serializer_class = ReservationSerializer

    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def get_fuerteventura_reservations(request):
        month = request.query_params.get('month', '2')
        year = request.query_params.get('year', '2025')
        
        try:
            # Find the FuerteVentura asset - adjust this query to match your data
            asset = Asset.objects.filter(nickname__icontains='fuerte').first()
            if not asset:
                return Response({'error': 'FuerteVentura asset not found'}, status=404)
            
            # Get reservations for the specified month and year
            reservations = Reservation.objects.filter(
                Q(asset=asset) &
                (
                    # Reservations that start in the target month
                    Q(entry_date__month=month, entry_date__year=year) |
                    # Reservations that end in the target month
                    Q(end_date__month=month, end_date__year=year)
                )
            ).order_by('entry_date')
            
            serializer = ReservationSerializer(reservations, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            return Response({'error': str(e)}, status=500)
    ```

12. Create URLs configuration in reservation_api/urls.py:
    ```bash
    nano reservation_api/urls.py
    ```

13. Add the following code:
    ```python
    from django.urls import path, include
    from rest_framework.routers import DefaultRouter
    from . import views

    router = DefaultRouter()
    router.register(r'assets', views.AssetViewSet)
    router.register(r'platforms', views.RentalPlatformViewSet)
    router.register(r'reservations', views.ReservationViewSet)

    urlpatterns = [
        path('', include(router.urls)),
        path('fuerteventura-reservations/', views.get_fuerteventura_reservations, name='fuerteventura-reservations'),
    ]
    ```

14. Update the project URLs in db_api/urls.py:
    ```bash
    nano db_api/urls.py
    ```

15. Add the following code:
    ```python
    from django.contrib import admin
    from django.urls import path, include
    from rest_framework.authtoken import views

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('api-auth/', include('rest_framework.urls')),
        path('api/', include('reservation_api.urls')),
    ]
    ```

16. Create a superuser for API authentication:
    ```bash
    python3 manage.py migrate
    python3 manage.py createsuperuser
    ```
    Follow the prompts to create a superuser with your desired credentials.

17. Create a script to start the API service:
    ```bash
    nano start_api.sh
    ```

18. Add the following content:
    ```bash
    #!/bin/bash
    cd ~/db_api_service
    python3 manage.py runserver 0.0.0.0:8000
    ```

19. Make the script executable:
    ```bash
    chmod +x start_api.sh
    ```

20. Create a systemd service file to run the API service:
    ```bash
    sudo nano /etc/systemd/system/db-api.service
    ```

21. Add the following content:
    ```
    [Unit]
    Description=Database API Service
    After=network.target

    [Service]
    User=pi
    WorkingDirectory=/home/pi/db_api_service
    ExecStart=/home/pi/db_api_service/start_api.sh
    Restart=on-failure
    RestartSec=5

    [Install]
    WantedBy=multi-user.target
    ```

22. Enable and start the service:
    ```bash
    sudo systemctl enable db-api.service
    sudo systemctl start db-api.service
    ```

23. Check the service status:
    ```bash
    sudo systemctl status db-api.service
    ```

## Testing the API

1. Test the API on the local machine:
   ```bash
   curl -u username:password http://localhost:8000/api/fuerteventura-reservations/
   ```
   Replace username:password with the superuser credentials you created.

2. Verify that the API returns the expected JSON data containing the February 2025 reservations for the FuerteVentura property.

## Troubleshooting Database Connectivity

If you encounter connection issues with the existing database:

1. Verify that the database connection settings are correct:
   - IP address of the Raspberry Pi 3B
   - Database name
   - Username and password
   - Port number

2. Check if PostgreSQL is listening on the expected IP address:
   ```bash
   ssh username@192.168.2.10
   sudo -u postgres psql -c "SHOW listen_addresses;"
   ```

3. Check if the PostgreSQL configuration allows connections from the Raspberry Pi 4:
   ```bash
   ssh username@192.168.2.10
   sudo cat /etc/postgresql/13/main/pg_hba.conf | grep 192.168.1.10
   ```
   You should see a line allowing connections from the Raspberry Pi 4's IP address.

4. Test the direct database connection from the Raspberry Pi 4:
   ```bash
   PGPASSWORD=your_password psql -h 192.168.2.10 -U your_username -d your_database -c "SELECT 1;"
   ```
   If this works, you should see a result of "1".

## Next Steps

Now that the connection to the database server is established and the API is working, proceed to the [Web Application Server Implementation](./01c_Web_Application.md) document to set up the web application server with Django and React frontend. 