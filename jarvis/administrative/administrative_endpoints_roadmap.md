# Administrative Application API Endpoints Roadmap

This document outlines the RESTful API endpoints for the Administrative application, following best practices for API design and Domain-Driven Design principles.

## Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Insurance Company Endpoints](#insurance-company-endpoints)
4. [Insurance Contract Endpoints](#insurance-contract-endpoints)
5. [Document Endpoints](#document-endpoints)
6. [File Management Endpoints](#file-management-endpoints)
7. [Error Handling](#error-handling)
8. [API Versioning](#api-versioning)

## Overview

The Administrative API provides endpoints for managing insurance-related documents, contracts, and files. It follows REST principles and implements CRUD operations for all resources.

## Authentication

All endpoints require authentication using token-based authentication provided by Django REST Framework.

```python
# Example views.py authentication setup
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class BaseAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
```

## Insurance Company Endpoints

### Model Fields
- name (CharField): Company name
- phone_number (PositiveIntegerField): Contact phone number
- site_app_company (CharField): Website or application URL

### Endpoints

#### List and Create Insurance Companies
- **URL**: `/api/administrative/insurance-companies/`
- **Methods**: GET, POST
- **Permissions**: IsAuthenticated
- **Response Format**:
  ```json
  [
    {
      "id": 1,
      "name": "Example Insurance Co",
      "phone_number": 5555555555,
      "site_app_company": "exampleinsurance.com",
      "url": "/api/administrative/insurance-companies/1/"
    }
  ]
  ```

#### Retrieve, Update, Delete Insurance Company
- **URL**: `/api/administrative/insurance-companies/{id}/`
- **Methods**: GET, PUT, PATCH, DELETE
- **Permissions**: IsAuthenticated

## Insurance Contract Endpoints

### Model Fields
- company (ForeignKey): Reference to InsuranceCompany
- type (CharField): Type of insurance (Real Estate, Transportation, Person)
- real_estate_asset (ForeignKey): Associated real estate asset
- transportation_asset (ForeignKey): Associated transportation asset
- person (ForeignKey): Associated user
- contract_number (CharField): Contract identifier
- starting_date (DateField): Contract start date
- ending_date (DateField): Contract end date
- is_insurance_active (BooleanField): Active status
- personal_email_used (EmailField): Contact email
- annual_price (JSONField): Yearly pricing information
- coverage (JSONField): Coverage details

### Endpoints

#### List and Create Insurance Contracts
- **URL**: `/api/administrative/insurance-contracts/`
- **Methods**: GET, POST
- **Query Parameters**:
  - `company`: Filter by insurance company ID
  - `type`: Filter by insurance type
  - `active`: Filter by active status
  - `user`: Filter by associated user
- **Response Format**:
  ```json
  [
    {
      "id": 1,
      "company": {
        "id": 1,
        "name": "Example Insurance"
      },
      "type": "Real Estate insurance",
      "real_estate_asset": 2,
      "transportation_asset": null,
      "person": null,
      "contract_number": "INS-12345",
      "starting_date": "2023-01-01",
      "ending_date": "2024-01-01",
      "is_insurance_active": true,
      "personal_email_used": "user@example.com",
      "annual_price": {"2023": 400},
      "coverage": {"liability": "full coverage"},
      "url": "/api/administrative/insurance-contracts/1/"
    }
  ]
  ```

#### Retrieve, Update, Delete Insurance Contract
- **URL**: `/api/administrative/insurance-contracts/{id}/`
- **Methods**: GET, PUT, PATCH, DELETE
- **Permissions**: IsAuthenticated

#### Get Files Associated with Insurance Contract
- **URL**: `/api/administrative/insurance-contracts/{id}/files/`
- **Methods**: GET
- **Permissions**: IsAuthenticated

## Document Endpoints

### Model Fields
- user (ForeignKey): Associated user
- name (CharField): Document name
- type (CharField): Document type (ID card, Passport, etc.)
- comment (JSONField): Additional comments/metadata

### Endpoints

#### List and Create Documents
- **URL**: `/api/administrative/documents/`
- **Methods**: GET, POST
- **Query Parameters**:
  - `user`: Filter by user ID
  - `type`: Filter by document type
- **Response Format**:
  ```json
  [
    {
      "id": 1,
      "user": 1,
      "name": "Passport",
      "type": "Passport",
      "comment": {"expiry": "2025-01-01"},
      "url": "/api/administrative/documents/1/"
    }
  ]
  ```

#### Retrieve, Update, Delete Document
- **URL**: `/api/administrative/documents/{id}/`
- **Methods**: GET, PUT, PATCH, DELETE
- **Permissions**: IsAuthenticated

#### Get Files Associated with Document
- **URL**: `/api/administrative/documents/{id}/files/`
- **Methods**: GET
- **Permissions**: IsAuthenticated

## File Management Endpoints

### Base File Model Fields
- name (CharField): File name
- content (FileField): File content

### File Document Model
- access_to_model (ForeignKey): Associated Document

### File Insurance Contract Model
- access_to_model (ForeignKey): Associated InsuranceContract

### Endpoints

#### List and Upload Files
- **URL**: `/api/administrative/files/`
- **Methods**: GET, POST
- **Permissions**: IsAuthenticated
- **Response Format**:
  ```json
  [
    {
      "id": 1,
      "name": "document.pdf",
      "content": "http://example.com/media/files/document.pdf",
      "url": "/api/administrative/files/1/"
    }
  ]
  ```

#### Retrieve, Update, Delete File
- **URL**: `/api/administrative/files/{id}/`
- **Methods**: GET, PUT, PATCH, DELETE
- **Permissions**: IsAuthenticated

#### Upload Document File
- **URL**: `/api/administrative/documents/{document_id}/files/`
- **Methods**: POST
- **Permissions**: IsAuthenticated

#### Upload Insurance Contract File
- **URL**: `/api/administrative/insurance-contracts/{contract_id}/files/`
- **Methods**: POST
- **Permissions**: IsAuthenticated

## Error Handling

All endpoints should return appropriate HTTP status codes:

- 200: OK
- 201: Created
- 204: No Content
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error

Error responses should follow a consistent format:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable error message",
    "details": {}
  }
}
```

## API Versioning

API versioning should be implemented using URL versioning:

```
/api/v1/administrative/...
```

## Implementation Guidelines

1. **Serializers**: Create serializers for each model with appropriate validation
2. **ViewSets**: Use Django REST Framework ViewSets for CRUD operations
3. **Filtering**: Implement filtering using Django REST Framework's filter backends
4. **Pagination**: Implement pagination for list endpoints
5. **Testing**: Write comprehensive tests for all endpoints
6. **Documentation**: Use Django REST Framework's built-in documentation tools

### Example Implementation Structure

```
administrative/
├── api/
│   ├── serializers/
│   │   ├── __init__.py
│   │   ├── document_serializers.py
│   │   ├── file_serializers.py
│   │   ├── insurance_company_serializers.py
│   │   └── insurance_contract_serializers.py
│   ├── views/
│   │   ├── __init__.py
│   │   ├── document_views.py
│   │   ├── file_views.py
│   │   ├── insurance_company_views.py
│   │   └── insurance_contract_views.py
│   ├── urls.py
│   └── __init__.py
└── ...
``` 