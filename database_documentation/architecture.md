# System Architecture

This document outlines the system architecture of the Personal Asset Management System, including its components, interactions, and design principles.

## Architecture Overview

The system is built using a modular Django architecture, with separate apps for different functional domains. Each app maintains its own models, views, and business logic, while sharing core infrastructure components.

### High-Level Architecture Diagram

```
+------------------------+      +------------------+
|  Web Interface (UI)    |<---->|  Django Core     |
+------------------------+      +------------------+
                                        |
                                        v
 +---------------------------------------------------+
 |                                                   |
 |  +----------------+  +---------------+  +------+  |
 |  | Administrative |  | Financial     |  | Real  |  |
 |  | Module         |  | Module        |  | Estate|  |
 |  +----------------+  +---------------+  +------+  |
 |                                                   |
 |  +----------------+  +---------------+  +------+  |
 |  | Transportation |  | Health        |  | Tax   |  |
 |  | Module         |  | Module        |  | Module|  |
 |  +----------------+  +---------------+  +------+  |
 |                                                   |
 +---------------------------------------------------+
                      |
                      v
          +----------------------+
          |  PostgreSQL Database |
          +----------------------+
```

## Core Components

### 1. Django Framework

The system is built on Django, using:
- Django ORM for database interactions
- Django Admin for administrative interfaces
- Django Templates for rendering views
- Django Authentication for user management

### 2. Module Structure

The system is divided into the following Django apps:

#### Administrative Module
- **Purpose**: Core user management, document handling, and authentication
- **Key Models**: Document, File
- **Dependencies**: None (base module)

#### Financial Module
- **Purpose**: Banking accounts, cards, and financial reporting
- **Key Models**: Bank, BankAccount, BankCard, BankAccountReport
- **Dependencies**: Administrative Module

#### Real Estate Module
- **Purpose**: Property management, rental contracts, and utilities
- **Key Models**: Asset, Bill, CoproManagementContract, HollydaysReservation, Mortgage, RentingManagementContract, Tenant, UtilityContract
- **Dependencies**: Financial Module

#### Transportation Module
- **Purpose**: Vehicle and transportation asset management
- **Key Models**: TransportationAsset, File
- **Dependencies**: Administrative Module

#### Health Module
- **Purpose**: Health expenses, insurance, and product tracking
- **Key Models**: HealthBill, Product, Symptom
- **Dependencies**: Administrative Module

#### Tax Module
- **Purpose**: Tax record keeping and management
- **Key Models**: Tax, TaxManagementCompany, TaxManagementContract
- **Dependencies**: Real Estate Module, Transportation Module, Administrative Module

### 3. Insurance System

The insurance component spans multiple modules:
- **Purpose**: Track different types of insurance (real estate, transportation, personal)
- **Key Models**: InsuranceCompany, InsuranceContract
- **Dependencies**: All domain modules

## Data Flow

1. **User Input Flow**:
   - User interacts with the Django Admin interface
   - Input is validated by model field validators
   - Data is saved to the PostgreSQL database

2. **Document Storage Flow**:
   - Files are uploaded through file fields
   - Files are stored in the filesystem
   - File metadata and references are stored in the database

3. **Reporting Flow**:
   - Data is aggregated from multiple models
   - Reports are generated using database queries
   - Results are presented in the Django Admin interface

## Technology Stack

- **Backend**: Django (Python)
- **Database**: PostgreSQL
- **Containerization**: Docker & Docker Compose
- **Web Server**: Gunicorn (with optional Nginx reverse proxy)
- **Development Tools**: Django Debug Toolbar, development environment settings

## Design Patterns

The system implements several design patterns:

1. **Repository Pattern**: 
   - Django models and managers act as repositories
   - Centralized data access logic

2. **Inheritance Hierarchy**:
   - Base File model with specialized file models for different domains

3. **Composition**:
   - Complex domain objects (like Asset) composed of multiple related entities

4. **Domain-Driven Design**:
   - Each module represents a bounded context
   - Rich domain models with behavior and validation

## Security Architecture

The system implements security at multiple levels:

1. **Authentication**: Django's authentication system
2. **Authorization**: Permission-based access control
3. **Data Protection**: Sensitive data stored securely
4. **Input Validation**: Through Django's form and model validation

## Deployment Architecture

### Docker Deployment

```
+---------------------+     +--------------------+
| Nginx Container     |<--->| Django Container   |
| (Reverse Proxy)     |     | (Gunicorn)         |
+---------------------+     +--------------------+
                                     |
                                     v
                            +--------------------+
                            | PostgreSQL         |
                            | Container          |
                            +--------------------+
                                     |
                                     v
                            +--------------------+
                            | Persistent Volume  |
                            | (Data & Files)     |
                            +--------------------+
```

### Standalone Deployment

```
+------------------+     +------------------+
| Django           |<--->| PostgreSQL       |
| (Web Server)     |     | (Database)       |
+------------------+     +------------------+
         |
         v
+------------------+
| Filesystem       |
| (Media & Static) |
+------------------+
```

## Extension Points

The system is designed to be extensible:

1. New asset types can be added with minimal changes
2. Additional financial instruments can be accommodated
3. Reporting capabilities can be extended
4. Third-party integrations can be added

## Future Architecture Considerations

Potential future enhancements:

1. **API Layer**: REST API for mobile app integration
2. **Message Queue**: Asynchronous processing for background tasks
3. **Caching Layer**: Redis for improved performance
4. **Analytics**: Data warehouse for complex reporting
5. **Mobile App**: Native mobile application for field access 