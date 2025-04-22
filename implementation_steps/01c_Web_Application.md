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
   mkdir -p ~/AI4Devs-Final-Project
   cd ~/AI4Devs-Final-Project
   mkdir -p jarvis UI
   ```

## Backend Container Configuration

Instead of creating a new Django application, we'll use the existing backend application that already has the Health app with the Symptom model. We'll set up a Docker container for it.

1. Set up the backend directory:
   ```bash
   cd ~/AI4Devs-Final-Project/jarvis
   ```

2. Create a Dockerfile for the backend (if not already present):
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

7. Create or update the project's settings to work with the containerized setup:

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

8. Ensure the Health app has a properly configured API endpoint for Symptoms:
   
   The API endpoints are defined in `jarvis/health/api/urls.py`. The endpoint structure should be:
   ```python
   router.register(r'symptoms', SymptomViewSet, basename='symptom')
   ```

9. Test the API endpoint by running the development server:
   ```bash
   cd ~/AI4Devs-Final-Project
   ./start_api.sh
   ```
   
   And accessing: http://localhost:8000/api/health/symptoms/
   
   If everything works as expected, you can stop the development server.

## Frontend Container Implementation

Now we'll create a separate React frontend container that will communicate with the Django backend.

1. Navigate to the frontend directory:
   ```bash
   cd ~/AI4Devs-Final-Project/UI
   ```

2. Create a Dockerfile for the React frontend (if not already present):
   ```bash
   nano Dokerfile
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

9. Create the api.ts file in the app/src directory:
   ```bash
   nano app/src/api.ts
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
        const response = await axios.get(`${API_URL}/api/health/symptoms/`);
        return response.data;
      } catch (error) {
        console.error('Error fetching symptoms:', error);
        throw error;
      }
    };
    ```

11. Create a components directory if it doesn't exist:
    ```bash
    mkdir -p app/src/components
    ```

12. Create a SymptomTable component:
    ```bash
    nano app/src/components/SymptomTable.tsx
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

14. Update the existing App component:
    ```bash
    nano app/src/App.tsx
    ```

15. Replace the content with the following:
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

16. Update the existing App.css file:
    ```bash
    nano app/src/App.css
    ```

17. Replace the content with the following styles:
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

18. Verify the structure of main.tsx file:
    ```bash
    nano app/src/main.tsx
    ```

19. If needed, update main.tsx with the following content (if it differs significantly):
    ```tsx
    import { StrictMode } from 'react'
    import { createRoot } from 'react-dom/client'
    import './index.css'
    import App from './App.tsx'

    createRoot(document.getElementById('root')!).render(
      <StrictMode>
        <App />
      </StrictMode>,
    )
    ```

20. Update the api.ts file to include any additional API functions needed:
    ```bash
    nano app/src/api.ts
    ```

21. Modify vite.config.ts to include the API proxy:
    ```bash
    nano app/vite.config.ts
    ```
    
    ```typescript
    import { defineConfig } from 'vite'
    import react from '@vitejs/plugin-react'

    // https://vite.dev/config/
    export default defineConfig({
      plugins: [react()],
      server: {
        proxy: {
          '/api': {
            target: 'http://localhost:8000',
            changeOrigin: true
          }
        }
      }
    })
    ```

## Docker Compose Setup

1. Navigate back to the project root:
   ```bash
   cd ~/AI4Devs-Final-Project
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
       build: ./jarvis
       restart: always
       volumes:
         - static_volume:/app/staticfiles
         - backend_data:/app/data
       env_file:
         - ./jarvis/.env
       depends_on:
         - redis
       expose:
         - 8000
       networks:
         - app_network

     # Frontend service
     frontend:
       build: ./UI
       restart: always
       depends_on:
         - backend
       expose:
         - 80
       networks:
         - app_network

     # Redis service for caching
     redis:
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

## Implementation Status

Below is a status table showing the progress of each step in the web application implementation:

| Section | Step | Status | Comments |
|---------|------|--------|----------|
| **Docker Installation** | Install Docker | ✅ | |
| | Add user to Docker group | ✅ | |
| | Verify Docker installation | ✅ | |
| | Install Docker Compose | ✅ | |
| | Verify Docker Compose installation | ✅ | |
| **Project Directory Setup** | Create project directories | ✅ | |
| **Backend Container Configuration** | Setup backend directory | ✅ | |
| | Create Dockerfile | ✅ | |
| | Create requirements.txt | ✅ | |
| | Create .env file | ✅ | |
| | Configure Django settings | ✅ | |
| | Test API endpoint | ❌ | Currently experiencing 400 Bad Request errors when accessing API endpoints |
| **Frontend Container Implementation** | Create Dockerfile | ✅ | |
| | Create nginx configuration | ✅ | |
| | Initialize React application | ✅ | |
| | Install dependencies | ✅ | |
| | Create API interface | ✅ | |
| | Create SymptomTable component | ✅ | |
| | Update App component | ✅ | |
| | Configure Vite | ✅ | |
| **Docker Compose Setup** | Create docker-compose.yml | ✅ | |
| **Building and Running the Application** | Build and start containers | ✅ | |
| | Verify container status | ✅ | |
| | Access web application | ❌ | Web application UI is accessible but API requests to backend are failing with 400 Bad Request |
| **Testing the Application** | Verify health symptoms display | ❌ | Cannot display health symptoms due to API communication issues |
| | Verify database connection | ❌ | Unable to verify due to API communication issues |
| | Verify container operation | ✅ | All containers are running but there are issues with the backend API |
| **Container Management** | Container operations knowledge | ✅ | |
| **Troubleshooting** | Initial diagnostics performed | ✅ | Several debugging scripts have been developed to diagnose the API issues |
| **Next Steps** | Public Access Configuration | ❌ | Blocked by current API communication issues |

**Current Focus**: 
- Resolving 400 Bad Request errors when accessing the Django backend API endpoints
- Diagnosing potential CORS or configuration issues in the Django application
- Testing direct access to API endpoints through both the nginx proxy and directly to the backend 