# Personal Database Assistant

A secure, internet-accessible chatbot interface to query health symptoms data stored in a PostgreSQL database on Raspberry Pi 3B.

## Project Overview

This project provides a chatbot interface for users to query their health data. It consists of several components:

- React-based frontend with chatbot interface
- Django REST API backend
- API Bridge for secure database communication
- Nginx for web serving and routing

All components are containerized using Docker for easy deployment and maintenance.

## Project Structure

```
personal-database-assistant/
│
├── docker-compose.yml              # Main container orchestration
├── README.md                       # Project documentation
├── .env                            # Environment variables (gitignored)
├── .gitignore                      # Git ignore file
│
├── frontend/                       # React frontend application
│   ├── Dockerfile                  # Frontend container config
│   ├── package.json                # NPM dependencies
│   ├── public/                     # Static assets
│   └── src/                        # Source code
│       ├── components/             # React components
│       │   ├── App.js              # Main application component
│       │   ├── ChatInterface.js    # Chatbot UI component
│       │   ├── MessageList.js      # Chat message display component
│       │   └── MessageInput.js     # User input component
│       ├── services/               # API services
│       │   └── chatService.js      # Service for chat API communication
│       ├── styles/                 # CSS styles
│       │   └── main.css            # Main stylesheet
│       └── index.js                # Application entry point
│
├── backend/                        # Django backend application
│   ├── Dockerfile                  # Backend container config
│   ├── requirements.txt            # Python dependencies
│   ├── entrypoint.sh               # Container entrypoint script
│   ├── personal_db_assistant/      # Django project
│   │   ├── settings.py             # Project settings
│   │   ├── urls.py                 # URL routing
│   │   └── wsgi.py                 # WSGI configuration
│   └── api/                        # Django app for API
│
├── api_bridge/                     # API Bridge for secure DB communication
│   ├── Dockerfile                  # API Bridge container config
│   ├── requirements.txt            # Python dependencies
│   ├── app.py                      # Main application
│   ├── db_connector.py             # Database connection handler
│   └── security.py                 # Security-related functionality
│
├── nginx/                          # Nginx web server configuration
│   ├── Dockerfile                  # Nginx container config
│   ├── nginx.conf                  # Main configuration
│   └── ssl/                        # SSL certificate files (gitignored)
│
└── documentation/                  # Project documentation
    ├── container_logging.md        # Container logging documentation
    └── test_scripts/               # Testing scripts
```

## Architecture

```
Internet ---> Nginx (Raspberry Pi 4) ---> Frontend ---> Backend ---> API Bridge ---> Database (Raspberry Pi 3B)
```

## Development Setup

1. Clone the repository
2. Create a `.env` file based on the example provided
3. Run `docker-compose up --build` to start all services
4. Access the application at http://localhost:8080

## Container Health Checks

The application includes comprehensive health checks for all containers to ensure automatic restart if any service becomes unhealthy.

## Container Logging

Structured logging is implemented across all containers for easy monitoring and troubleshooting.

## Production Deployment

For production deployment:

1. Update the `.env` file with production values
2. Ensure SSL certificates are in place
3. Run `docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d`

## Security Considerations

- All communication between components is secured
- Database credentials are managed via environment variables
- API Bridge provides an additional security layer for database access 