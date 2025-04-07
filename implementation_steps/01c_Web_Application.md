# Web Application Server Implementation

This document outlines the steps to set up the web application server on the Raspberry Pi 4, which will host the containerized Django backend, React frontend, and supporting services for displaying health symptoms and related products.

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

## Backend Container Configuration

Instead of creating a new Django application, we'll use the existing backend application that already has the Health app with the Symptom model. We'll set up a Docker container for it.

1. Clone the existing backend repository:
   ```bash
   cd ~/personal-db-assistant
   git clone [REPOSITORY_URL] backend
   cd backend
   ```

2. Create a Dockerfile for the existing backend:
   ```bash
   nano Dockerfile
   ```

3. Add the following content:
   ```dockerfile
   FROM python:3.10-slim-buster

   WORKDIR /app

   ENV PYTHONDONTWRITEBYTECODE=1
   ENV PYTHONUNBUFFERED=1

   RUN apt-get update && apt-get install -y --no-install-recommends \
       gcc \
       && rm -rf /var/lib/apt/lists/*

   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   COPY . .

   EXPOSE 8000

   # Adjust the command based on your project's actual WSGI application path
   CMD ["gunicorn", "--bind", "0.0.0.0:8000", "jarvis.wsgi:application"]
   ```

4. If the project doesn't already have a requirements.txt file, create one:
   ```bash
   pip freeze > requirements.txt
   ```
   
   Or create one manually with the minimum required packages:
   ```bash
   nano requirements.txt
   ```
   
   And add:
   ```
   Django==4.2.10
   djangorestframework==3.14.0
   django-cors-headers==4.3.1
   gunicorn==21.2.0
   python-dotenv==1.0.0
   psycopg2-binary==2.9.9
   redis==5.0.1
   ```

5. Create a .env file for environment variables:
   ```bash
   nano .env
   ```

6. Add the following content in your .env file (update with your actual values):
   ```
   DEBUG=False
   SECRET_KEY=your-secure-secret-key
   ALLOWED_HOSTS=localhost,127.0.0.1,192.168.1.10,your-domain.com,backend
   REDIS_URL=redis://redis:6379/1
   ```

7. Create or update the project's settings to work with the containerized setup. This might involve creating a separate settings file for Docker or modifying the existing settings:

   ```bash
   nano jarvis/settings.py
   ```
   
   Add or update the following configurations:
   
   ```python
   # Add the following imports at the top if they don't exist
   import os
   from pathlib import Path
   from dotenv import load_dotenv
   
   # Load environment variables
   load_dotenv()
   
   # Update ALLOWED_HOSTS
   ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
   
   # Add or update CORS settings
   CORS_ALLOW_ALL_ORIGINS = False
   CORS_ALLOWED_ORIGINS = [
       "http://localhost:3000",
       "http://localhost:8000",
       "http://localhost",
       "http://frontend:3000",  # Allow the frontend container
       "http://frontend:80",    # Allow the frontend container in production
   ]
   
   # Add Redis cache configuration
   CACHES = {
       "default": {
           "BACKEND": "django.core.cache.backends.redis.RedisCache",
           "LOCATION": os.environ.get('REDIS_URL', 'redis://redis:6379/1'),
       }
   }
   ```

8. Ensure the Health app has a properly configured API endpoint for Symptoms. If it doesn't exist, create a REST API endpoint.

   First, check if the app already has serializers:
   ```bash
   ls jarvis/health/serializers.py
   ```
   
   If not, create one:
   ```bash
   nano jarvis/health/serializers.py
   ```
   
   Add the following content:
   ```python
   from rest_framework import serializers
   from .models.symptom import Symptom
   from .models.product import Product
   
   class ProductSerializer(serializers.ModelSerializer):
       class Meta:
           model = Product
           fields = ['id', 'name']
   
   class SymptomSerializer(serializers.ModelSerializer):
       products = ProductSerializer(many=True, read_only=True)
       
       class Meta:
           model = Symptom
           fields = ['id', 'name', 'child', 'adult', 'products', 'comments']
   ```

9. Create or update the API views for the Health app:
   ```bash
   nano jarvis/health/views.py
   ```
   
   Add the following content:
   ```python
   from rest_framework import viewsets
   from rest_framework.response import Response
   from .models.symptom import Symptom
   from .serializers import SymptomSerializer
   from django.views.decorators.cache import cache_page
   from django.utils.decorators import method_decorator
   
   class SymptomViewSet(viewsets.ReadOnlyModelViewSet):
       queryset = Symptom.objects.all().prefetch_related('products')
       serializer_class = SymptomSerializer
       
       @method_decorator(cache_page(60 * 5))  # Cache for 5 minutes
       def list(self, request, *args, **kwargs):
           return super().list(request, *args, **kwargs)
       
       @method_decorator(cache_page(60 * 5))
       def retrieve(self, request, *args, **kwargs):
           return super().retrieve(request, *args, **kwargs)
   ```

10. Add URL patterns for the API:
    ```bash
    nano jarvis/health/urls.py
    ```
    
    Add the following content:
    ```python
    from django.urls import path, include
    from rest_framework.routers import DefaultRouter
    from .views import SymptomViewSet
    
    router = DefaultRouter()
    router.register(r'symptoms', SymptomViewSet)
    
    urlpatterns = [
        path('', include(router.urls)),
    ]
    ```

11. Finally, include the Health app URLs in the main project URLs:
    ```bash
    nano jarvis/urls.py
    ```
    
    Ensure the following pattern is included:
    ```python
    urlpatterns = [
        # ... other patterns ...
        path('api/health/', include('jarvis.health.urls')),
    ]
    ```

12. Test the API endpoint by running the development server:
    ```bash
    python manage.py runserver
    ```
    
    And accessing: http://localhost:8000/api/health/symptoms/
    
    If everything works as expected, you can stop the development server.

These steps configure the existing backend application to work within a Docker container and expose the necessary API endpoints for our frontend to consume the Symptoms data.

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
   COPY --from=build /app/dist /usr/share/nginx/html

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

6. Initialize a new React application using Vite:
   ```bash
   # Use a temporary Node container to create the React app with Vite
   docker run --rm -v $(pwd):/app -w /app node:18-alpine sh -c "npx create-vite@latest . --template react-ts"
   ```

7. Install dependencies:
   ```bash
   docker run --rm -v $(pwd):/app -w /app node:18-alpine npm install
   ```

8. Install additional dependencies:
   ```bash
   docker run --rm -v $(pwd):/app -w /app node:18-alpine npm install axios bootstrap react-bootstrap react-router-dom
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

    // Interface for Symptom data
    export interface Symptom {
      id: number;
      name: string;
      child: boolean;
      adult: boolean;
      products: Product[];
      comments: Record<string, string> | null;
    }

    // Interface for Product data
    export interface Product {
      id: number;
      name: string;
    }

    // Function to fetch symptoms
    export const fetchSymptoms = async (): Promise<Symptom[]> => {
      try {
        const response = await axios.get(`${API_URL}/api/symptoms/`);
        return response.data;
      } catch (error) {
        console.error('Error fetching symptoms:', error);
        throw error;
      }
    };
    ```

11. Create a src/components directory:
    ```bash
    mkdir -p src/components
    ```

12. Create a SymptomTable component:
    ```bash
    nano src/components/SymptomTable.tsx
    ```

13. Add the following content:
    ```tsx
    import React, { useEffect, useState } from 'react';
    import { Table, Spinner, Alert, Badge } from 'react-bootstrap';
    import { fetchSymptoms, Symptom } from '../api';

    const SymptomTable: React.FC = () => {
      const [symptoms, setSymptoms] = useState<Symptom[]>([]);
      const [loading, setLoading] = useState<boolean>(true);
      const [error, setError] = useState<string | null>(null);

      useEffect(() => {
        const loadSymptoms = async () => {
          try {
            const data = await fetchSymptoms();
            setSymptoms(data);
            setLoading(false);
          } catch (err) {
            setError('Failed to load symptoms from database');
            setLoading(false);
          }
        };

        loadSymptoms();
      }, []);

      if (loading) return <div className="text-center mt-5"><Spinner animation="border" /></div>;
      if (error) return <Alert variant="danger">{error}</Alert>;
      if (symptoms.length === 0) return <Alert variant="info">No symptoms found in the database</Alert>;

      return (
        <Table striped bordered hover responsive>
          <thead>
            <tr>
              <th>Name</th>
              <th>Applicable To</th>
              <th>Products</th>
              <th>Comments</th>
            </tr>
          </thead>
          <tbody>
            {symptoms.map(symptom => (
              <tr key={symptom.id}>
                <td>{symptom.name}</td>
                <td>
                  {symptom.adult && <Badge bg="primary" className="me-1">Adult</Badge>}
                  {symptom.child && <Badge bg="info">Child</Badge>}
                </td>
                <td>
                  {symptom.products.map(product => (
                    <Badge key={product.id} bg="secondary" className="me-1">{product.name}</Badge>
                  ))}
                </td>
                <td>
                  {symptom.comments && (
                    <ul className="list-unstyled mb-0">
                      {Object.entries(symptom.comments).map(([key, value]) => (
                        <li key={key}><strong>{key}:</strong> {value}</li>
                      ))}
                    </ul>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
      );
    };

    export default SymptomTable;
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
    import SymptomTable from './components/SymptomTable';
    import './App.css';

    function App() {
      return (
        <div className="App">
          <Navbar bg="dark" variant="dark">
            <Container>
              <Navbar.Brand href="/">Health Symptoms Database</Navbar.Brand>
            </Container>
          </Navbar>
          
          <Container className="mt-4">
            <Card>
              <Card.Header>
                <h2>Health Symptoms and Recommended Products</h2>
              </Card.Header>
              <Card.Body>
                <SymptomTable />
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
      background-color: #198754; /* Green color for health theme */
      color: white;
    }

    .table {
      margin-bottom: 0;
    }

    .table th {
      background-color: #e9ecef;
    }

    .badge {
      font-size: 0.85em;
    }
    ```

18. Update the main.tsx file (Vite uses main.tsx instead of index.tsx):
    ```bash
    nano src/main.tsx
    ```

19. Replace with the following content:
    ```tsx
    import React from 'react'
    import ReactDOM from 'react-dom/client'
    import App from './App.tsx'
    import './index.css'

    ReactDOM.createRoot(document.getElementById('root')!).render(
      <React.StrictMode>
        <App />
      </React.StrictMode>,
    )
    ```

20. Update the vite.config.ts file:
    ```bash
    nano vite.config.ts
    ```

21. Add the following content:
    ```typescript
    import { defineConfig } from 'vite'
    import react from '@vitejs/plugin-react'

    // https://vitejs.dev/config/
    export default defineConfig({
      plugins: [react()],
      server: {
        proxy: {
          '/api': {
            target: 'http://backend:8000',
            changeOrigin: true
          }
        }
      }
    })
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
2. Verify that the health symptoms and related products are displayed.
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
   - Database API connectivity: `curl -u username:password http://192.168.2.10:8000/api/health/symptoms/`

2. If no data is displayed, check:
   - Backend API response: `curl http://localhost/api/api/symptoms/`
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