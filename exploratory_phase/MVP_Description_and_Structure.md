# Personal Database Assistant - MVP Description and Structure

## MVP Overview

The Minimum Viable Product (MVP) for the Personal Database Assistant focuses on providing a secure, internet-accessible chatbot interface to query health symptoms data stored in an existing database on Raspberry Pi 3B.

### Core MVP Features

1. **Internet-Accessible Frontend UI**
   - Simple React-based frontend with chatbot interface
   - Basic responsive design for different devices
   - Minimal styling focused on functionality

2. **Health Symptoms Data Retrieval**
   - Chatbot capable of understanding queries about health symptoms
   - Secure connection to existing database on Raspberry Pi 3B
   - Simple response formatting for readability

3. **Backend Implementation**
   - Basic Django REST API without authentication
   - Secure API bridge to communicate with Raspberry Pi 3B database
   - Simple integration with PostgreSQL database

4. **Infrastructure**
   - Docker container setup (Frontend, Backend, API Bridge, Nginx)
   - Secure network configuration between Raspberry Pi 4 and 3B
   - Simple deployment process

### MVP Limitations

- No authentication or authorization
- No data privacy vault
- No document processing or email integration
- No financial data visualization
- Minimal security measures (basic HTTPS and secure database connection)

## Project File Structure

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
│   ├── manage.py                   # Django management script
│   ├── personal_db_assistant/      # Django project
│   │   ├── settings.py             # Project settings
│   │   ├── urls.py                 # URL routing
│   │   └── wsgi.py                 # WSGI configuration
│   └── api/                        # Django app for API
│       ├── models.py               # Data models
│       ├── serializers.py          # REST serializers
│       ├── views.py                # API views/endpoints
│       ├── services/               # Business logic services
│       │   ├── query_processor.py  # NLP query processing
│       │   └── data_service.py     # Data retrieval service
│       └── tests/                  # Unit tests
│
├── api_bridge/                     # API Bridge for secure DB communication
│   ├── Dockerfile                  # API Bridge container config
│   ├── requirements.txt            # Python dependencies
│   ├── app.py                      # Main application
│   ├── db_connector.py             # Database connection handler
│   └── security.py                 # Security-related functionality
│
└── nginx/                          # Nginx web server configuration
    ├── Dockerfile                  # Nginx container config
    ├── nginx.conf                  # Main configuration
    └── ssl/                        # SSL certificate files (gitignored)
```

## Architecture Diagram

```
Internet ---> Nginx (Raspberry Pi 4) ---> Frontend ---> Backend ---> API Bridge ---> Database (Raspberry Pi 3B)
```

## Technology Stack

- **Frontend**: React, JavaScript, CSS
- **Backend**: Django, Django REST Framework
- **API Bridge**: Python, psycopg2
- **Database**: PostgreSQL (existing on Raspberry Pi 3B)
- **Web Server**: Nginx
- **Containerization**: Docker, Docker Compose
- **Deployment**: Raspberry Pi 4 (Internet-facing server)

## Development Workflow

1. Set up Docker environment on Raspberry Pi 4
2. Configure secure connection to PostgreSQL on Raspberry Pi 3B
3. Develop backend API for health symptoms data
4. Implement API bridge for secure database communication
5. Create frontend chatbot interface
6. Configure Nginx for web serving and routing
7. Test end-to-end functionality
8. Deploy MVP to production environment

## Next Steps After MVP

Upon successful implementation of the MVP, the project will progressively add:

1. **Layer 1**: Authentication and authorization
2. **Layer 2**: Financial data access
3. **Layer 3**: Synthetic financial data
4. **Layer 4**: Financial data visualization 