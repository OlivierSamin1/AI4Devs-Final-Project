# Jarvis - Personal Database Assistant

## Overview

Jarvis is a personal database assistant designed to help users manage and query personal data across various domains including:

- Health information
- Financial records
- Real estate data
- Tax information
- Transportation records
- Administrative documents

The system is built as a modern web application with a chatbot interface that allows users to ask natural language questions about their personal data.

## Architecture

The project follows a microservices architecture with Docker containers:

### Backend (Django REST API)
- Built with Django 4.2 and Django REST Framework
- PostgreSQL database connectivity
- Modular design with separate domain apps (finances, health, tax, etc.)
- Custom middleware for request handling and debugging

### Frontend (React)
- React 19 with TypeScript
- Bootstrap for responsive UI
- React Router for navigation
- Axios for API communication

### Deployment
- Docker containerization
- Nginx as reverse proxy and static file server
- SSL/TLS configuration for secure communication

## Project Structure

```
├── jarvis/                   # Django backend
│   ├── administrative/       # Administrative domain
│   ├── finances/             # Financial domain
│   ├── health/               # Health domain
│   ├── real_estate/          # Real estate domain
│   ├── tax/                  # Tax domain
│   ├── transportation/       # Transportation domain
│   └── jarvis/               # Main Django project files
├── UI/                       # React frontend
│   ├── app/                  # React application
│   │   ├── src/              # React source code
│   │   └── public/           # Public assets
│   ├── nginx.conf            # Nginx configuration
│   └── Dockerfile            # Frontend Docker config
├── docker-compose.yml        # Container orchestration
└── Dockerfile                # Backend Docker config
```

## Development Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/AI4Devs-Final-Project.git
   cd AI4Devs-Final-Project
   ```

2. Environment setup:
   Create a `.env` file in the `jarvis/` directory with:
   ```
   DEBUG=True
   SECRET_KEY=your_secret_key
   DATABASE_URL=postgres://user:password@host:port/database
   ```

3. Start the development environment:
   ```
   docker-compose up -d
   ```

4. Access the application:
   - Frontend: http://jarvis.localhost or http://localhost
   - Backend API: http://jarvis.localhost/api/

## User Stories and Requirements

The project follows a sprint-based development approach with user stories grouped by domain and functionality. See the `User_stories` directory for detailed requirements and sprint planning.

## License

This project is licensed under the terms included in the LICENSE file.

## Changes Made for Container Health Checks Implementation

- **Implemented Health Checks**: Added health check endpoints for Django and Nginx to monitor their statuses.
- **Docker Configuration**: Updated `docker-compose.yml` to include health check configurations for both services.
- **Database Connection Check**: Enhanced the `check_database_connection()` function in `container_health.py` to use environment variables directly and improve error detection.
- **Test Script Improvements**: Updated `test_health_checks.sh` to provide better diagnostics and ensure environment variables are correctly used.
- **Documentation**: Updated relevant documentation to reflect the changes made in the health checks implementation.

### Summary of Health Check Features
- Health checks for database, disk space, and memory usage.
- Automatic restart of unhealthy containers based on health check results.

