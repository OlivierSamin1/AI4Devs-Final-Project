# Health Application API Endpoints Roadmap

This document outlines the RESTful API endpoints for the Health application, following best practices for API design and Domain-Driven Design principles.

## Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Product Endpoints](#product-endpoints)
4. [Symptom Endpoints](#symptom-endpoints)
5. [Bill Endpoints](#bill-endpoints)
6. [File Management Endpoints](#file-management-endpoints)
7. [Error Handling](#error-handling)
8. [API Versioning](#api-versioning)

## Overview

The Health API provides endpoints for managing health-related products, symptoms, bills, and files. It follows REST principles and implements CRUD operations for all resources.

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

## Product Endpoints

### Model Fields
- name (CharField): Product name
- natural (BooleanField): Whether the product is natural
- child_use (BooleanField): Whether the product is for children
- adult_use (BooleanField): Whether the product is for adults
- min_age (CharField): Minimum age for use
- source_info (CharField): Source of product information
- date_info (DateField): Date of information
- composition (CharField): Product composition
- interests (CharField): Usage interests
- comments (JSONField): Additional comments/metadata

### Endpoints

#### List and Create Products
- **URL**: `/api/health/products/`
- **Methods**: GET, POST
- **Permissions**: IsAuthenticated
- **Response Format**:
  ```json
  [
    {
      "id": 1,
      "name": "Example Product",
      "natural": true,
      "child_use": false,
      "adult_use": true,
      "min_age": "18",
      "source_info": "Medical Journal",
      "date_info": "2023-01-01",
      "composition": "Natural ingredients",
      "interests": "Pain relief",
      "comments": {"usage": "Take twice daily", "side_effects": "None known"},
      "url": "/api/health/products/1/"
    }
  ]
  ```

#### Retrieve, Update, Delete Product
- **URL**: `/api/health/products/{id}/`
- **Methods**: GET, PUT, PATCH, DELETE
- **Permissions**: IsAuthenticated

#### Get Files Associated with Product
- **URL**: `/api/health/products/{id}/files/`
- **Methods**: GET
- **Permissions**: IsAuthenticated

## Symptom Endpoints

### Model Fields
- name (CharField): Symptom name
- child (BooleanField): Whether applies to children
- adult (BooleanField): Whether applies to adults
- products (ManyToManyField): Associated products
- comments (JSONField): Additional information

### Endpoints

#### List and Create Symptoms
- **URL**: `/api/health/symptoms/`
- **Methods**: GET, POST
- **Query Parameters**:
  - `name`: Filter by name
  - `child`: Filter by child applicability
  - `adult`: Filter by adult applicability
  - `product`: Filter by associated product
- **Response Format**:
  ```json
  [
    {
      "id": 1,
      "name": "Headache",
      "child": true,
      "adult": true,
      "products": [1, 2],
      "comments": {"severity": "mild to severe", "duration": "varies"},
      "url": "/api/health/symptoms/1/"
    }
  ]
  ```

#### Retrieve, Update, Delete Symptom
- **URL**: `/api/health/symptoms/{id}/`
- **Methods**: GET, PUT, PATCH, DELETE
- **Permissions**: IsAuthenticated

#### Get Files Associated with Symptom
- **URL**: `/api/health/symptoms/{id}/files/`
- **Methods**: GET
- **Permissions**: IsAuthenticated

#### Get Products for Symptom
- **URL**: `/api/health/symptoms/{id}/products/`
- **Methods**: GET
- **Permissions**: IsAuthenticated

## Bill Endpoints

### Model Fields
- company_name (CharField): Healthcare provider name
- client_name (ForeignKey): Associated user
- bill_name (CharField): Name of the bill
- date (DateField): Date of bill
- total_price (FloatField): Total cost
- is_paid (BooleanField): Payment status
- is_asked_by_us (BooleanField): Whether requested by the organization

### Endpoints

#### List and Create Bills
- **URL**: `/api/health/bills/`
- **Methods**: GET, POST
- **Query Parameters**:
  - `company_name`: Filter by company name
  - `client_name`: Filter by client
  - `is_paid`: Filter by payment status
  - `date_after`: Filter by date after
  - `date_before`: Filter by date before
- **Response Format**:
  ```json
  [
    {
      "id": 1,
      "company_name": "Example Healthcare",
      "client_name": {
        "id": 1,
        "username": "user1"
      },
      "bill_name": "Annual Checkup",
      "date": "2023-05-15",
      "total_price": 150.00,
      "is_paid": true,
      "is_asked_by_us": false,
      "url": "/api/health/bills/1/"
    }
  ]
  ```

#### Retrieve, Update, Delete Bill
- **URL**: `/api/health/bills/{id}/`
- **Methods**: GET, PUT, PATCH, DELETE
- **Permissions**: IsAuthenticated

#### Get Files Associated with Bill
- **URL**: `/api/health/bills/{id}/files/`
- **Methods**: GET
- **Permissions**: IsAuthenticated

## File Management Endpoints

### Base File Model Fields
- name (CharField): File name
- content (FileField): File content

### FileBill Model
- access_to_model (ForeignKey): Associated Bill

### FileProduct Model
- access_to_model (ForeignKey): Associated Product

### FileSymptom Model
- access_to_model (ForeignKey): Associated Symptom

### Endpoints

#### List and Upload Files
- **URL**: `/api/health/files/`
- **Methods**: GET, POST
- **Permissions**: IsAuthenticated
- **Response Format**:
  ```json
  [
    {
      "id": 1,
      "name": "medical_document.pdf",
      "content": "http://example.com/media/files/medical_document.pdf",
      "url": "/api/health/files/1/"
    }
  ]
  ```

#### Retrieve, Update, Delete File
- **URL**: `/api/health/files/{id}/`
- **Methods**: GET, PUT, PATCH, DELETE
- **Permissions**: IsAuthenticated

#### Upload Bill File
- **URL**: `/api/health/bills/{bill_id}/files/`
- **Methods**: POST
- **Permissions**: IsAuthenticated

#### Upload Product File
- **URL**: `/api/health/products/{product_id}/files/`
- **Methods**: POST
- **Permissions**: IsAuthenticated

#### Upload Symptom File
- **URL**: `/api/health/symptoms/{symptom_id}/files/`
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
/api/v1/health/...
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
health/
├── api/
│   ├── serializers/
│   │   ├── __init__.py
│   │   ├── product_serializers.py
│   │   ├── symptom_serializers.py
│   │   ├── bill_serializers.py
│   │   └── file_serializers.py
│   ├── views/
│   │   ├── __init__.py
│   │   ├── product_views.py
│   │   ├── symptom_views.py
│   │   ├── bill_views.py
│   │   └── file_views.py
│   ├── urls.py
│   └── __init__.py
└── ...
``` 