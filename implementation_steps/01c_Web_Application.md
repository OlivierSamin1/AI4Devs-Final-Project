# Web Application Server Implementation

This document outlines the steps to set up the web application server on the Raspberry Pi 4, which will host the containerized Django backend, React frontend, and supporting services for displaying the FuerteVentura property reservations.

## Prerequisites

Ensure you have completed the [Hardware Setup](./01a_Hardware_Setup.md) and [Database Server Connection](./01b_Database_Server.md) steps before proceeding. Remember that the database server on Raspberry Pi 3B is already configured and contains the necessary data.

## Docker Installation

We'll use Docker to containerize our entire application stack for easier deployment and management.

1. Install Docker on the Raspberry Pi 4:
   ```bash
   curl -sSL https://get.docker.com | sh
   ```

2. Add the Pi user to the Docker group:
   ```bash
   sudo usermod -aG docker $USER
   ```

3. Log out and log back in for the group changes to take effect:
   ```bash
   logout
   ```

4. After logging back in, verify Docker installation:
   ```bash
   docker --version
   ```

5. Install Docker Compose:
   ```bash
   sudo apt-get install -y python3-pip
   sudo pip3 install docker-compose
   ```

6. Verify Docker Compose installation:
   ```bash
   docker-compose --version
   ```

## Project Directory Setup

1. Create a project directory structure:
   ```bash
   mkdir -p ~/personal-db-assistant
   cd ~/personal-db-assistant
   mkdir -p backend frontend nginx redis
   ```

## Backend Container Implementation

### Django Project Setup

1. Create a requirements.txt file in the backend directory:
   ```bash
   nano backend/requirements.txt
   ```

2. Add the following dependencies:
   ```
   Django==4.2.10
   djangorestframework==3.14.0
   django-cors-headers==4.3.1
   requests==2.31.0
   gunicorn==21.2.0
   python-dotenv==1.0.0
   psycopg2-binary==2.9.9
   redis==5.0.1
   ```

3. Create a Dockerfile for the backend:
   ```bash
   nano backend/Dockerfile
   ```

4. Add the following content:
   ```dockerfile
   FROM python:3.10-slim-buster

   WORKDIR /app

   ENV PYTHONDONTWRITEBYTECODE 1
   ENV PYTHONUNBUFFERED 1

   RUN apt-get update && apt-get install -y --no-install-recommends \
       gcc \
       && rm -rf /var/lib/apt/lists/*

   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   COPY . .

   EXPOSE 8000

   CMD ["gunicorn", "--bind", "0.0.0.0:8000", "web_app.wsgi:application"]
   ```

5. Create the Django project:
   ```bash
   cd backend
   docker run --rm -v $(pwd):/app -w /app python:3.10-slim-buster pip install django==4.2.10
   docker run --rm -v $(pwd):/app -w /app python:3.10-slim-buster django-admin startproject web_app .
   ```

6. Create a Django app for the dashboard:
   ```bash
   docker run --rm -v $(pwd):/app -w /app python:3.10-slim-buster python manage.py startapp dashboard
   ```

### Backend Configuration

1. Edit the Django settings:
   ```bash
   nano web_app/settings.py
   ```

2. Update the settings:
   ```python
   import os
   from pathlib import Path

   # Build paths inside the project like this: BASE_DIR / 'subdir'.
   BASE_DIR = Path(__file__).resolve().parent.parent

   # SECURITY WARNING: keep the secret key used in production secret!
   SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-default-key-for-development')

   # SECURITY WARNING: don't run with debug turned on in production!
   DEBUG = os.environ.get('DEBUG', 'False') == 'True'

   ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

   # Application definition
   INSTALLED_APPS = [
       'django.contrib.admin',
       'django.contrib.auth',
       'django.contrib.contenttypes',
       'django.contrib.sessions',
       'django.contrib.messages',
       'django.contrib.staticfiles',
       'rest_framework',
       'corsheaders',
       'dashboard',
   ]

   MIDDLEWARE = [
       'django.middleware.security.SecurityMiddleware',
       'django.contrib.sessions.middleware.SessionMiddleware',
       'corsheaders.middleware.CorsMiddleware',
       'django.middleware.common.CommonMiddleware',
       'django.middleware.csrf.CsrfViewMiddleware',
       'django.contrib.auth.middleware.AuthenticationMiddleware',
       'django.contrib.messages.middleware.MessageMiddleware',
       'django.middleware.clickjacking.XFrameOptionsMiddleware',
   ]

   ROOT_URLCONF = 'web_app.urls'

   TEMPLATES = [
       {
           'BACKEND': 'django.template.backends.django.DjangoTemplates',
           'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

   WSGI_APPLICATION = 'web_app.wsgi.application'

   # Database - we're using SQLite for the web app's local storage needs
   # The actual property data comes from the external Raspberry Pi 3B database via API
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.sqlite3',
           'NAME': BASE_DIR / 'db.sqlite3',
       }
   }

   # Redis cache configuration
   CACHES = {
       "default": {
           "BACKEND": "django.core.cache.backends.redis.RedisCache",
           "LOCATION": os.environ.get('REDIS_URL', 'redis://redis:6379/1'),
       }
   }

   # Password validation
   # https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
   AUTH_PASSWORD_VALIDATORS = [
       {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
       {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
       {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
       {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
   ]

   # Internationalization
   # https://docs.djangoproject.com/en/4.2/topics/i18n/
   LANGUAGE_CODE = 'en-us'
   TIME_ZONE = 'UTC'
   USE_I18N = True
   USE_TZ = True

   # Static files (CSS, JavaScript, Images)
   # https://docs.djangoproject.com/en/4.2/howto/static-files/
   STATIC_URL = 'static/'
   STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
   STATICFILES_DIRS = [
       os.path.join(BASE_DIR, 'static'),
   ]

   # Default primary key field type
   # https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
   DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

   # CORS settings
   CORS_ALLOW_ALL_ORIGINS = False
   CORS_ALLOWED_ORIGINS = [
       "http://localhost:3000",
       "http://localhost:8000",
       "http://localhost",
       "http://frontend:3000",  # Allow the frontend container
   ]

   # Database API settings - update these with your actual credentials
   DB_API_BASE_URL = os.environ.get('DB_API_BASE_URL', 'http://192.168.2.10:8000/api')
   DB_API_USERNAME = os.environ.get('DB_API_USERNAME', 'api_user')
   DB_API_PASSWORD = os.environ.get('DB_API_PASSWORD', 'api_password')
   ```

3. Create an API client for communicating with the database server:
   ```bash
   nano dashboard/api_client.py
   ```

4. Add the following code:
   ```python
   import requests
   from django.conf import settings
   import logging

   logger = logging.getLogger(__name__)

   class DatabaseAPIClient:
       def __init__(self):
           self.base_url = settings.DB_API_BASE_URL
           self.auth = (settings.DB_API_USERNAME, settings.DB_API_PASSWORD)
       
       def _make_request(self, method, endpoint, params=None, data=None):
           url = f"{self.base_url}/{endpoint}"
           
           try:
               response = requests.request(
                   method,
                   url,
                   auth=self.auth,
                   params=params,
                   json=data,
                   timeout=10
               )
               response.raise_for_status()
               return response.json()
           except requests.exceptions.RequestException as e:
               logger.error(f"API request error: {e}")
               return None
       
       def get_fuerteventura_reservations(self, month=2, year=2025):
           """Fetch February 2025 reservations for FuerteVentura property from the existing database API"""
           return self._make_request('GET', 'fuerteventura-reservations/', params={'month': month, 'year': year})
   ```

5. Create views in dashboard/views.py:
   ```bash
   nano dashboard/views.py
   ```

6. Add the following code:
   ```python
   from django.shortcuts import render
   from django.http import JsonResponse
   from .api_client import DatabaseAPIClient
   from datetime import datetime
   from django.views.decorators.cache import cache_page

   def home(request):
       return render(request, 'dashboard/home.html')

   @cache_page(60 * 5)  # Cache for 5 minutes
   def reservations_api(request):
       # Get query parameters with defaults set for February 2025
       month = request.GET.get('month', '2')
       year = request.GET.get('year', '2025')
       
       # Use API client to fetch data from the existing database
       client = DatabaseAPIClient()
       reservations = client.get_fuerteventura_reservations(month, year)
       
       if reservations is None:
           return JsonResponse({'error': 'Failed to fetch reservations from database server'}, status=500)
       
       return JsonResponse(reservations, safe=False)
   ```

7. Create the URLs for the dashboard app in dashboard/urls.py:
   ```bash
   nano dashboard/urls.py
   ```

8. Add the following code:
   ```python
   from django.urls import path
   from . import views

   urlpatterns = [
       path('', views.home, name='home'),
       path('api/reservations/', views.reservations_api, name='reservations_api'),
   ]
   ```

9. Update the project URLs in web_app/urls.py:
   ```bash
   nano web_app/urls.py
   ```

10. Add the following code:
    ```python
    from django.contrib import admin
    from django.urls import path, include
    from django.conf import settings
    from django.conf.urls.static import static

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('api/', include('dashboard.urls')),
    ]

    if settings.DEBUG:
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    ```

11. Create a static directory:
    ```bash
    mkdir -p static/css
    ```

12. Create a simple CSS file in static/css/style.css:
    ```bash
    nano static/css/style.css
    ```

13. Add some basic styles:
    ```css
    body {
        background-color: #f8f9fa;
    }

    .card {
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .card-header {
        background-color: #007bff;
        color: white;
    }

    .table {
        margin-bottom: 0;
    }

    .table th {
        background-color: #e9ecef;
    }
    ```

14. Create a .env file for environment variables:
    ```bash
    nano .env
    ```

15. Add the following content (update with your actual values for the existing database API):
    ```
    DEBUG=False
    SECRET_KEY=your-secure-secret-key
    ALLOWED_HOSTS=localhost,127.0.0.1,192.168.1.10,your-domain.com,backend
    DB_API_BASE_URL=http://192.168.2.10:8000/api
    DB_API_USERNAME=your_api_username
    DB_API_PASSWORD=your_api_password
    REDIS_URL=redis://redis:6379/1
    ```

## Frontend Container Implementation

Now we'll create a separate React frontend container that will communicate with the Django backend.

1. Navigate to the frontend directory:
   ```bash
   cd ~/personal-db-assistant/frontend
   ```

2. Create a Dockerfile for the React frontend:
   ```bash
   nano Dockerfile
   ```

3. Add the following content:
   ```dockerfile
   # Build stage
   FROM node:18-alpine as build

   WORKDIR /app

   # Copy package files and install dependencies
   COPY package*.json ./
   RUN npm install

   # Copy the rest of the application and build
   COPY . ./
   RUN npm run build

   # Production stage
   FROM nginx:alpine

   # Copy the build output from the build stage
   COPY --from=build /app/build /usr/share/nginx/html

   # Copy custom nginx config
   COPY ./nginx.conf /etc/nginx/conf.d/default.conf

   EXPOSE 80

   CMD ["nginx", "-g", "daemon off;"]
   ```

4. Create a custom nginx configuration for the frontend:
   ```bash
   nano nginx.conf
   ```

5. Add the following content:
   ```nginx
   server {
       listen 80;
       
       location / {
           root /usr/share/nginx/html;
           index index.html index.htm;
           try_files $uri $uri/ /index.html;
       }

       # Proxy requests to the backend API
       location /api/ {
           proxy_pass http://backend:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

6. Initialize a new React application using create-react-app:
   ```bash
   # Use a temporary Node container to create the React app
   docker run --rm -v $(pwd):/app -w /app node:18-alpine sh -c "npx create-react-app . --template typescript"
   ```

7. Create a package.json file:
   ```bash
   nano package.json
   ```

8. Update the package.json with necessary dependencies:
   ```json
   {
     "name": "personal-db-assistant-frontend",
     "version": "0.1.0",
     "private": true,
     "dependencies": {
       "@testing-library/jest-dom": "^5.17.0",
       "@testing-library/react": "^13.4.0",
       "@testing-library/user-event": "^13.5.0",
       "@types/jest": "^27.5.2",
       "@types/node": "^16.18.40",
       "@types/react": "^18.2.20",
       "@types/react-dom": "^18.2.7",
       "axios": "^1.4.0",
       "bootstrap": "^5.3.1",
       "react": "^18.2.0",
       "react-bootstrap": "^2.8.0",
       "react-dom": "^18.2.0",
       "react-router-dom": "^6.15.0",
       "react-scripts": "5.0.1",
       "typescript": "^4.9.5",
       "web-vitals": "^2.1.4"
     },
     "scripts": {
       "start": "react-scripts start",
       "build": "react-scripts build",
       "test": "react-scripts test",
       "eject": "react-scripts eject"
     },
     "eslintConfig": {
       "extends": [
         "react-app",
         "react-app/jest"
       ]
     },
     "browserslist": {
       "production": [
         ">0.2%",
         "not dead",
         "not op_mini all"
       ],
       "development": [
         "last 1 chrome version",
         "last 1 firefox version",
         "last 1 safari version"
       ]
     }
   }
   ```

9. Create a src/api.ts file:
   ```bash
   mkdir -p src
   nano src/api.ts
   ```

10. Add the following content:
    ```typescript
    import axios from 'axios';

    // Base URL for the API
    const API_URL = '/api';

    // Interface for Reservation data
    export interface Reservation {
      id: number;
      asset_id: number;
      asset_name: string;
      platform_id: number;
      platform_name: string;
      reservation_number: string;
      entry_date: string;
      end_date: string;
      number_of_nights: number;
      renting_person_full_name: string;
      price: string;
      created_at: string;
    }

    // Function to fetch reservations
    export const fetchReservations = async (month: number = 2, year: number = 2025): Promise<Reservation[]> => {
      try {
        const response = await axios.get(`${API_URL}/api/reservations/`, {
          params: { month, year }
        });
        return response.data;
      } catch (error) {
        console.error('Error fetching reservations:', error);
        throw error;
      }
    };
    ```

11. Create a src/components directory:
    ```bash
    mkdir -p src/components
    ```

12. Create a ReservationTable component:
    ```bash
    nano src/components/ReservationTable.tsx
    ```

13. Add the following content:
    ```tsx
    import React, { useEffect, useState } from 'react';
    import { Table, Spinner, Alert } from 'react-bootstrap';
    import { fetchReservations, Reservation } from '../api';

    const ReservationTable: React.FC = () => {
      const [reservations, setReservations] = useState<Reservation[]>([]);
      const [loading, setLoading] = useState<boolean>(true);
      const [error, setError] = useState<string | null>(null);

      useEffect(() => {
        const loadReservations = async () => {
          try {
            const data = await fetchReservations();
            setReservations(data);
            setLoading(false);
          } catch (err) {
            setError('Failed to load reservations from database');
            setLoading(false);
          }
        };

        loadReservations();
      }, []);

      if (loading) return <div className="text-center mt-5"><Spinner animation="border" /></div>;
      if (error) return <Alert variant="danger">{error}</Alert>;
      if (reservations.length === 0) return <Alert variant="info">No reservations found for February 2025</Alert>;

      return (
        <Table striped bordered hover responsive>
          <thead>
            <tr>
              <th>Check-in Date</th>
              <th>Check-out Date</th>
              <th>Nights</th>
              <th>Guest</th>
              <th>Platform</th>
              <th>Reservation #</th>
              <th>Price</th>
            </tr>
          </thead>
          <tbody>
            {reservations.map(reservation => (
              <tr key={reservation.id}>
                <td>{new Date(reservation.entry_date).toLocaleDateString()}</td>
                <td>{new Date(reservation.end_date).toLocaleDateString()}</td>
                <td>{reservation.number_of_nights}</td>
                <td>{reservation.renting_person_full_name}</td>
                <td>{reservation.platform_name}</td>
                <td>{reservation.reservation_number}</td>
                <td>${parseFloat(reservation.price).toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </Table>
      );
    };

    export default ReservationTable;
    ```

14. Create the App component:
    ```bash
    nano src/App.tsx
    ```

15. Add the following content:
    ```tsx
    import React from 'react';
    import 'bootstrap/dist/css/bootstrap.min.css';
    import { Container, Navbar, Card } from 'react-bootstrap';
    import ReservationTable from './components/ReservationTable';
    import './App.css';

    function App() {
      return (
        <div className="App">
          <Navbar bg="dark" variant="dark">
            <Container>
              <Navbar.Brand href="/">Personal DB Assistant</Navbar.Brand>
            </Container>
          </Navbar>
          
          <Container className="mt-4">
            <Card>
              <Card.Header>
                <h2>FuerteVentura Reservations - February 2025</h2>
              </Card.Header>
              <Card.Body>
                <ReservationTable />
              </Card.Body>
            </Card>
          </Container>
        </div>
      );
    }

    export default App;
    ```

16. Create a simple CSS file for the App:
    ```bash
    nano src/App.css
    ```

17. Add some basic styles:
    ```css
    .App {
      min-height: 100vh;
      background-color: #f8f9fa;
    }

    .card {
      margin-bottom: 20px;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .card-header {
      background-color: #007bff;
      color: white;
    }

    .table {
      margin-bottom: 0;
    }

    .table th {
      background-color: #e9ecef;
    }
    ```

18. Update the index.tsx file:
    ```bash
    nano src/index.tsx
    ```

19. Replace with the following content:
    ```tsx
    import React from 'react';
    import ReactDOM from 'react-dom/client';
    import './index.css';
    import App from './App';
    import reportWebVitals from './reportWebVitals';

    const root = ReactDOM.createRoot(
      document.getElementById('root') as HTMLElement
    );
    root.render(
      <React.StrictMode>
        <App />
      </React.StrictMode>
    );

    // If you want to start measuring performance in your app, pass a function
    // to log results (for example: reportWebVitals(console.log))
    // or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
    reportWebVitals();
    ```

## Redis Container Configuration

1. Navigate to the redis directory:
   ```bash
   cd ~/personal-db-assistant/redis
   ```

2. Create a custom redis.conf file:
   ```bash
   nano redis.conf
   ```

3. Add the following configuration:
   ```
   # Basic configuration
   port 6379
   bind 0.0.0.0
   protected-mode yes
   requirepass redispassword

   # Limits
   maxmemory 256mb
   maxmemory-policy allkeys-lru

   # Persistence
   save 900 1
   save 300 10
   save 60 10000
   ```

## Nginx Container Configuration

1. Navigate to the nginx directory:
   ```bash
   cd ~/personal-db-assistant/nginx
   ```

2. Create a Dockerfile for Nginx:
   ```bash
   nano Dockerfile
   ```

3. Add the following content:
   ```dockerfile
   FROM nginx:alpine

   COPY ./default.conf /etc/nginx/conf.d/default.conf
   ```

4. Create a Nginx configuration file:
   ```bash
   nano default.conf
   ```

5. Add the following configuration:
   ```nginx
   # Main proxy server for the application
   server {
       listen 80;
       server_name localhost;

       # Serve static files directly from the backend
       location /static/ {
           proxy_pass http://backend:8000/static/;
       }

       # Pass API requests to the backend
       location /api/ {
           proxy_pass http://backend:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }

       # Route all other requests to the frontend
       location / {
           proxy_pass http://frontend:80;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

## Docker Compose Setup

1. Navigate back to the project root:
   ```bash
   cd ~/personal-db-assistant
   ```

2. Create a docker-compose.yml file:
   ```bash
   nano docker-compose.yml
   ```

3. Add the following configuration:
   ```yaml
   version: '3'

   services:
     # Backend API service
     backend:
       build: ./backend
       restart: always
       volumes:
         - static_volume:/app/staticfiles
         - backend_data:/app/data
       env_file:
         - ./backend/.env
       depends_on:
         - redis
       expose:
         - 8000
       networks:
         - app_network

     # Frontend service
     frontend:
       build: ./frontend
       restart: always
       depends_on:
         - backend
       expose:
         - 80
       networks:
         - app_network

     # Redis service for caching
     redis:
       build: ./redis
       image: redis:alpine
       restart: always
       command: redis-server /usr/local/etc/redis/redis.conf
       volumes:
         - ./redis/redis.conf:/usr/local/etc/redis/redis.conf
         - redis_data:/data
       expose:
         - 6379
       networks:
         - app_network

     # Main web server
     nginx:
       build: ./nginx
       restart: always
       volumes:
         - static_volume:/app/staticfiles
       ports:
         - "80:80"
       depends_on:
         - backend
         - frontend
       networks:
         - app_network

   volumes:
     static_volume:
     backend_data:
     redis_data:

   networks:
     app_network:
       driver: bridge
   ```

## Building and Running the Application

1. Ensure all files are in place:
   ```bash
   ls -la
   ```

2. Build and start the containers:
   ```bash
   docker-compose up -d --build
   ```

3. Check the container status:
   ```bash
   docker-compose ps
   ```

4. View the logs:
   ```bash
   docker-compose logs -f
   ```

5. Access the web application:
   - From the Raspberry Pi 4: http://localhost
   - From another device on the network: http://192.168.1.10

## Testing the Application

1. Check that the web application is accessible.
2. Verify that the FuerteVentura reservations are displayed for February 2025.
3. Check that the data is being retrieved from the existing database server on Raspberry Pi 3B.
4. Verify that all containers are running correctly: backend, frontend, nginx, and redis.

## Container Management

1. To stop the containers:
   ```bash
   docker-compose down
   ```

2. To restart the containers:
   ```bash
   docker-compose up -d
   ```

3. To view container logs:
   ```bash
   docker-compose logs -f [service_name]
   ```
   Where [service_name] can be backend, frontend, nginx, or redis.

4. To restart a specific container:
   ```bash
   docker-compose restart [service_name]
   ```

## Troubleshooting

1. If the web application is not accessible, check:
   - Docker container status: `docker-compose ps`
   - Docker logs: `docker-compose logs -f`
   - Network connectivity: `ping 192.168.2.10`
   - Database API connectivity: `curl -u username:password http://192.168.2.10:8000/api/fuerteventura-reservations/`

2. If no data is displayed, check:
   - Backend API response: `curl http://localhost/api/api/reservations/`
   - API client configuration in settings.py
   - Connection to the existing database server
   - Frontend network configuration

3. For container-specific issues:
   - Backend issues: `docker-compose logs backend`
   - Frontend issues: `docker-compose logs frontend`
   - Nginx issues: `docker-compose logs nginx`
   - Redis issues: `docker-compose logs redis`

## Next Steps

Now that the web application is set up with fully containerized backend and frontend components, proceed to the [Public Access Configuration](./01d_Public_Access.md) document to make the application accessible from the internet. 