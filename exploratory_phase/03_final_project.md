# Personal Database Assistant - Final Project Specification

## Project Overview

The Personal Database Assistant project aims to create a secure, internet-accessible interface to an existing offline personal database. The solution maintains strong security separation between the database (offline Raspberry Pi 3B) and the internet-facing application (Raspberry Pi 4) while providing AI-powered analytics, document processing, and email integration capabilities.

## System Architecture

### Hardware Components

1. **Database Server (Raspberry Pi 3B)**
   - Hosts the PostgreSQL database
   - Maintains full offline security
   - Provides API access only to authorized devices
   - Houses the Data Privacy Vault for sensitive information

2. **Web Application Server (Raspberry Pi 4)**
   - Internet-facing component
   - Hosts the web interface and application logic
   - Communicates with the database server via secure local network
   - Integrates with external services (OpenAI, Gmail)

### Network Architecture

```mermaid
graph TD
    subgraph "Internet"
        User[User\nBrowser]
        AI[AI Services\nOpenAI API]
        Gmail[Gmail API]
    end
    
    subgraph "Home Network"
        Router[Home Router\nWith Firewall]
        
        subgraph "DMZ VLAN"
            RPi4[Raspberry Pi 4\nIP: 192.168.1.x\nPort: 443]
        end
        
        subgraph "Secure VLAN"
            RPi3B[Raspberry Pi 3B\nIP: 192.168.2.x\nPort: 8000]
            DPV[Data Privacy Vault]
        end
    end
    
    User --> |HTTPS:443| Router
    AI <--> |HTTPS| RPi4
    Gmail <--> |HTTPS| RPi4
    
    Router --> |Port Forward\nHTTPS:443| RPi4
    RPi4 <--> |Internal API\nHTTP:8000| RPi3B
    RPi3B <--> DPV
    
    style Router fill:#f96,stroke:#333,stroke-width:2px
    style RPi4 fill:#9cf,stroke:#333,stroke-width:2px
    style RPi3B fill:#fcf,stroke:#333,stroke-width:2px
    style DPV fill:#fcf,stroke:#333,stroke-width:2px
```

## Technology Stack

### Backend (Raspberry Pi 4)
- **Django**: Core application framework
- **Django REST Framework**: For API endpoints consumption and creation
- **Celery**: Background task processing for documents and email integration
- **Redis**: Caching, message broker, and session storage
- **Nginx**: Web server with SSL termination
- **Let's Encrypt**: SSL certificate management

### Frontend (Raspberry Pi 4)
- **React**: Frontend framework for interactive user interface
- **TypeScript**: Type-safe JavaScript development
- **Plotly/Chart.js**: Data visualization components
- **Material-UI/Tailwind CSS**: UI component framework

### Database Server (Raspberry Pi 3B)
- **Django**: API interface to database
- **Django REST Framework**: RESTful API endpoints
- **PostgreSQL**: Primary database
- **pgcrypto**: Database encryption capabilities
- **Data Privacy Vault**: Specialized storage for sensitive personal data

### External Integrations
- **OpenAI API**: Natural language processing and AI assistant capabilities
- **Gmail API**: Email integration for document processing
- **OAuth 2.0**: Secure authentication for external services

## Core Functionality

### 1. AI Chatbot Interface
- Natural language processing for database queries
- Custom knowledge base connected to personal data
- Secure query execution against offline database
- Context-aware conversations about financial data and assets

### 2. Financial Dashboard
- Default visualizations (predefined reports)
- Dynamic visualization generation based on natural language requests
- Category management system for expense classification
- Data processing pipeline for financial analytics

### 3. Email Integration
- Gmail API integration for multiple accounts
- Email metadata indexing and search
- Label-based filtering and organization
- AI-powered email analysis and summarization

### 4. Document Processing
- Document upload and OCR capabilities
- Intelligent data extraction from documents
- Classification system for different document types
- Validation workflow before database insertion

## Data Privacy Vault Implementation

### Overview
The Data Privacy Vault (DPV) provides an additional layer of security for sensitive personal information, separating it from regular application data and implementing specialized encryption and access controls.

### Key Features

1. **Data Tokenization**
   - Replace sensitive data with non-sensitive tokens in main database
   - Original sensitive data stored only in the privacy vault
   - References maintained through secure token mapping

2. **Encryption Layers**
   - Field-level encryption for sensitive data
   - Separate encryption keys for different data categories
   - Key rotation capabilities for enhanced security

3. **Access Control**
   - Strict API-based access to sensitive data
   - Purpose-based access controls (e.g., display, reporting, analysis)
   - Comprehensive audit logging of all access requests

4. **Data Minimization**
   - Automatic data truncation where appropriate
   - Configurable data retention policies
   - Capability to anonymize historical data

### Implementation Approach

```mermaid
graph TD
    App[Application Layer] -->|Tokenized Request| API[Privacy Vault API]
    API -->|Authentication| AuthZ[Authorization Layer]
    AuthZ -->|Purpose Validation| Purpose[Purpose Validation]
    Purpose -->|Data Request| Store[Encrypted Data Store]
    Store -->|Encrypted Data| Crypto[Encryption/Decryption]
    Crypto -->|Decrypted Data| API
    API -->|Minimal Required Data| App
    
    Audit[Audit Logging] -.->|Log Access| API
    Config[Configuration & Policies] -.->|Apply Rules| Purpose
```

### Schema Design

The Data Privacy Vault will use a schema that separates data into sensitivity levels:

1. **Public Data**: Regular application data in main database (names, non-sensitive details)
2. **Protected Data**: Moderately sensitive information with basic encryption (addresses, contact details)
3. **Highly Sensitive Data**: Maximum protection with advanced encryption (financial account details, tax information)

## Synthetic Data Generation for Demo

### Requirements

To facilitate demonstrations while protecting real personal data, the system will include capabilities to generate and use synthetic data that:

1. **Mimics Production Structure**: Matches the schema and relationships of real data
2. **Provides Realistic Scenarios**: Generates plausible financial patterns and asset information
3. **Maintains Referential Integrity**: Ensures all relationships are properly maintained
4. **Is Clearly Identified**: Clearly marked as demo data throughout the interface

### Implementation Strategy

1. **Data Generation Framework**
   - Python-based synthetic data generation using libraries like Faker
   - Custom generators for domain-specific data (financial transactions, property details)
   - Configurable data volume and time periods

2. **Deployment Approach**
   - Separate "demo mode" configuration in the application
   - Ability to switch between production and demo databases
   - Visual indicators in UI when using demo data

3. **Demo Dataset Scope**
   - Multiple years of financial history
   - Various asset types (real estate, vehicles, investments)
   - Simulated email correspondence and documents
   - Realistic user activity patterns

### Demo Data Schema

```
- Users: 3-5 fictional users with different profiles
- Assets: 10-15 properties with different characteristics
- Financial Accounts: 5-10 accounts with transaction history
- Transactions: 1000+ transactions over 2-3 years
- Documents: 30-50 sample documents of different types
- Emails: 100+ email records with metadata and sample content
```

## Communication Between Raspberry Pis

### Approach

1. **REST API over Local Network**:
   - Secure REST API on the database Pi that only accepts local connections
   - API key authentication + IP restriction for all requests
   - HMAC request signing for tamper prevention

2. **Message Queue for Write Operations**:
   - Redis-based message queue for reliable write operations
   - Asynchronous processing for document uploads and complex operations
   - At-least-once delivery guarantee for critical operations

### Security Measures

1. **Network-Level Security**:
   - Separate VLAN for database server with strict firewall rules
   - No internet access for database server
   - MAC address filtering for additional security

2. **Application-Level Security**:
   - API key rotation schedule (monthly)
   - Request signing with timestamps to prevent replay attacks
   - Comprehensive request validation and sanitization

## Development and Deployment Plan

### Phase 1: Core Infrastructure

1. Set up Raspberry Pi hardware and network configuration
2. Configure VLAN separation and firewall rules
3. Implement basic API communication between servers
4. Set up authentication mechanisms
5. Implement Data Privacy Vault infrastructure

### Phase 2: Web Application Development

1. Develop Django backend for web server
2. Create React frontend with basic dashboard
3. Implement user authentication and authorization
4. Set up basic asset management functionality
5. Integrate synthetic data generation for demo mode

### Phase 3: External Integrations

1. Implement OpenAI API integration for natural language processing
2. Set up Gmail API integration for email processing
3. Develop document processing pipeline
4. Build AI-powered analytics capabilities

### Phase 4: Security Hardening and Testing

1. Conduct security audit and penetration testing
2. Implement additional security controls based on findings
3. Perform load testing and performance optimization
4. Finalize data privacy controls and audit logging

## Security Considerations

1. **Defense in Depth Strategy**:
   - Multiple security layers at network, application, and data levels
   - No single point of failure for security controls
   - Regular security audits and updates

2. **Data Protection**:
   - Encryption at rest for all sensitive data using Data Privacy Vault
   - Encryption in transit for all communications
   - Data minimization principles applied throughout

3. **Access Controls**:
   - Principle of least privilege for all operations
   - Role-based access control for web interface
   - Purpose-based access for sensitive data operations

4. **Compliance Readiness**:
   - GDPR-compatible data handling
   - Built-in data subject access request capabilities
   - Data minimization and retention controls

## Next Steps

1. **Detailed Technical Design**:
   - Database schema with privacy vault integration
   - API endpoint specifications
   - UI wireframes and component structure

2. **Development Environment Setup**:
   - Local development configuration
   - CI/CD pipeline for testing
   - Deployment automation scripts

3. **Implementation Prioritization**:
   - Core data management features first
   - Privacy vault integration early in development
   - External integrations after core functionality
   - Synthetic data generation for ongoing testing and demos 