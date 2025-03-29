# API Specification Document

## Overview

This document defines the RESTful API endpoints for the Personal Database Assistant that allows secure interaction with the offline database. The API facilitates communication between the internet-facing Raspberry Pi 4 (web server) and the offline Raspberry Pi 3B (database server).

## Base URL

All API endpoints are relative to the base URL:

- Internal Network: `http://[raspberry-pi-3b-ip]:8000/api/v1/`

## Authentication

### Authentication Methods

The API uses two authentication mechanisms:

1. **API Key Authentication** (Primary method)
   - Required for all API requests
   - Must be included in the HTTP header: `Authorization: Api-Key <your_api_key>`
   - API keys are issued to the Raspberry Pi 4 and rotated periodically

2. **IP Restriction** (Secondary security layer)
   - API access is restricted to specific IP addresses (Raspberry Pi 4)
   - Requests from unauthorized IP addresses will be rejected regardless of valid API key

### Error Responses for Authentication

```json
{
  "status": "error",
  "code": 401,
  "message": "Authentication failed. Invalid API key."
}
```

## Data Format

- All requests and responses use JSON format
- UTF-8 encoding is required for all text data
- Dates should follow ISO 8601 format (YYYY-MM-DD)
- Timestamps should follow ISO 8601 with timezone (YYYY-MM-DDThh:mm:ss+zz:zz)

## Common Response Structure

All API responses follow a consistent structure:

```json
{
  "status": "success|error",
  "data": { ... },  // For successful responses
  "error": {        // For error responses
    "code": 400,
    "message": "Error description"
  }
}
```

## Endpoints

### Asset Management

#### List Assets

```
GET /assets/
```

Query Parameters:
- `type` (string, optional): Filter by asset type (real_estate, transportation)
- `owner_id` (integer, optional): Filter by owner ID
- `limit` (integer, optional): Maximum number of records to return (default: 20)
- `offset` (integer, optional): Number of records to skip (default: 0)
- `demo` (boolean, optional): If true, returns synthetic demo data instead of real data

Response:
```json
{
  "status": "success",
  "data": {
    "is_demo_data": false,
    "count": 5,
    "next": "/api/v1/assets/?offset=20&limit=20",
    "previous": null,
    "results": [
      {
        "id": 1,
        "nickname": "Fuerteventura Flat",
        "address": "123 Ocean View",
        "city": "Corralejo",
        "country": "Spain",
        "buying_date": "2019-05-15",
        "is_rented": true,
        "details": { ... }
      },
      // More assets
    ]
  }
}
```

#### Get Asset

```
GET /assets/{id}/
```

Query Parameters:
- `demo` (boolean, optional): If true, returns synthetic demo data instead of real data

Response:
```json
{
  "status": "success",
  "data": {
    "is_demo_data": false,
    "id": 1,
    "nickname": "Fuerteventura Flat",
    "address": "123 Ocean View",
    "postal_code": "35660",
    "city": "Corralejo",
    "country": "Spain",
    "buying_date": "2019-05-15",
    "buying_price": 180000,
    "has_on_going_mortgage": true,
    "is_rented": true,
    "is_our_living_house": false,
    "tax_management_id": 3,
    "details": {
      "bedrooms": 2,
      "bathrooms": 1,
      "surface": 85
    },
    "results_by_year": {
      "2022": {
        "rental_income": 15000,
        "expenses": 3500,
        "profit": 11500
      },
      "2023": {
        "rental_income": 16500,
        "expenses": 3800,
        "profit": 12700
      }
    }
  }
}
```

#### Create Asset

```
POST /assets/
```

Request:
```json
{
  "owner_id": 1,
  "nickname": "Mountain Cabin",
  "address": "45 Alpine Road",
  "postal_code": "74500",
  "city": "Chamonix",
  "country": "France",
  "buying_date": "2023-11-10",
  "buying_price": 320000,
  "has_on_going_mortgage": true,
  "is_rented": false,
  "is_our_living_house": false,
  "details": {
    "bedrooms": 3,
    "bathrooms": 2,
    "surface": 110
  }
}
```

Response:
```json
{
  "status": "success",
  "data": {
    "id": 6,
    "owner_id": 1,
    "nickname": "Mountain Cabin",
    // Other fields as in the request
  }
}
```

#### Update Asset

```
PUT /assets/{id}/
```

Request: Same format as Create Asset
Response: Same format as Get Asset

#### Delete Asset

```
DELETE /assets/{id}/
```

Response:
```json
{
  "status": "success",
  "data": {
    "message": "Asset successfully deleted"
  }
}
```

### Financial Module

#### List Bank Accounts

```
GET /bank-accounts/
```

Query Parameters:
- `demo` (boolean, optional): If true, returns synthetic demo data instead of real data

Response structure similar to List Assets.

#### Get Bank Account

```
GET /bank-accounts/{id}/
```

Query Parameters:
- `demo` (boolean, optional): If true, returns synthetic demo data instead of real data

Response:
```json
{
  "status": "success",
  "data": {
    "is_demo_data": false,
    "id": 1,
    "bank_id": 3,
    "titular_id": 1,
    "name": "Main Checking Account",
    "IBAN": "FR76XXXXXXXXXXXXXXXX",
    "BIC": "BNPAFRPPXXX",
    "starting_date": "2018-03-15",
    "is_account_open": true,
    "value_on_31_12": {
      "2022": 12500.50,
      "2023": 15750.25
    }
  }
}
```

#### Bank Account Operations similar to Asset operations

### Real Estate Specific

#### Get Property Reservations

```
GET /assets/{asset_id}/reservations/
```

Query Parameters:
- `from_date` (date, optional): Start date for reservation period
- `to_date` (date, optional): End date for reservation period
- `demo` (boolean, optional): If true, returns synthetic demo data instead of real data

Response:
```json
{
  "status": "success",
  "data": {
    "is_demo_data": false,
    "asset": {
      "id": 1,
      "nickname": "Fuerteventura Flat"
    },
    "reservations": [
      {
        "id": 12,
        "platform_id": 2,
        "entry_date": "2023-07-15",
        "number_of_nights": 7,
        "end_date": "2023-07-22",
        "renting_person_full_name": "John Smith",
        "price": 895.00,
        "cleaning": 65.00,
        "commission_platform": 115.50
      },
      // More reservations
    ]
  }
}
```

### Document Management

#### List Documents

```
GET /documents/
```

Query Parameters:
- `type` (string, optional): Filter by document type
- `entity_type` (string, optional): Filter by related entity type (asset, bank_account, etc.)
- `entity_id` (integer, optional): Filter by related entity ID
- `demo` (boolean, optional): If true, returns synthetic demo data instead of real data

Response structure similar to List Assets.

#### Get Document

```
GET /documents/{id}/
```

Query Parameters:
- `demo` (boolean, optional): If true, returns synthetic demo data instead of real data

Response:
```json
{
  "status": "success",
  "data": {
    "is_demo_data": false,
    "id": 5,
    "name": "Rental Contract - Fuerteventura 2023",
    "type": "contract",
    "user_id": 1,
    "comment": {
      "notes": "Annual renewal, increased rate by 5%",
      "important_dates": ["2023-12-31"]
    },
    "files": [
      {
        "id": 15,
        "filename": "contract_2023.pdf",
        "file_url": "/api/v1/files/15/download/",
        "upload_date": "2023-01-10T09:15:30+01:00",
        "file_size": 1250000
      }
    ]
  }
}
```

#### Upload Document File

```
POST /documents/{document_id}/files/
```

Request: Multipart form data with file

Response:
```json
{
  "status": "success",
  "data": {
    "id": 16,
    "document_id": 5,
    "filename": "contract_appendix.pdf",
    "file_url": "/api/v1/files/16/download/",
    "upload_date": "2023-05-20T14:25:10+01:00",
    "file_size": 850000
  }
}
```

#### Download Document File

```
GET /files/{id}/download/
```

Response: File binary data with appropriate Content-Type header

### Email Integration Endpoints

#### List Email Metadata

```
GET /emails/
```

Query Parameters:
- `account` (string, optional): Email account
- `from_date` (date, optional): Filter by date range start
- `to_date` (date, optional): Filter by date range end
- `label` (string, optional): Filter by label/folder
- `demo` (boolean, optional): If true, returns synthetic demo data instead of real data

Response structure similar to other list endpoints.

#### Get Email

```
GET /emails/{id}/
```

Query Parameters:
- `demo` (boolean, optional): If true, returns synthetic demo data instead of real data

Response:
```json
{
  "status": "success",
  "data": {
    "is_demo_data": false,
    "id": "12345abcdef",
    "account": "personal@example.com",
    "subject": "Tax Statement 2023",
    "sender": "tax-office@government.org",
    "recipient": "personal@example.com",
    "date": "2023-04-15T10:30:25+01:00",
    "labels": ["Taxes", "Important"],
    "has_attachments": true,
    "snippet": "Your tax statement for 2023 is now available...",
    "attachments": [
      {
        "id": "attach123",
        "filename": "tax_statement_2023.pdf",
        "file_url": "/api/v1/emails/12345abcdef/attachments/attach123/",
        "file_size": 450000
      }
    ]
  }
}
```

### Data Privacy Vault Endpoints

#### Get Tokenized Data

```
GET /privacy-vault/tokens/{token}/
```

Request Headers:
- Required: `X-Purpose` header specifying the purpose of data access (display, reporting, analysis)

Response:
```json
{
  "status": "success",
  "data": {
    "token": "tkn_xyz123",
    "data_type": "bank_account_number",
    "value": "FR7612345678901234567890123",
    "masked_value": "FR76XXXXXXXXXXXX7890123",
    "access_level": "partial",
    "expires_at": "2023-12-31T23:59:59+01:00"
  }
}
```

#### Tokenize Sensitive Data

```
POST /privacy-vault/tokens/
```

Request:
```json
{
  "data_type": "bank_account_number",
  "value": "FR7612345678901234567890123",
  "access_policy": "standard",
  "expires_in_days": 90
}
```

Response:
```json
{
  "status": "success",
  "data": {
    "token": "tkn_abc789",
    "data_type": "bank_account_number",
    "masked_value": "FR76XXXXXXXXXXXX7890123",
    "expires_at": "2023-12-31T23:59:59+01:00"
  }
}
```

#### Update Token Access Policy

```
PUT /privacy-vault/tokens/{token}/access-policy/
```

Request:
```json
{
  "access_policy": "restricted",
  "expires_in_days": 30,
  "allowed_purposes": ["display", "audit"]
}
```

Response:
```json
{
  "status": "success",
  "data": {
    "token": "tkn_xyz123",
    "access_policy": "restricted",
    "allowed_purposes": ["display", "audit"],
    "expires_at": "2023-09-30T23:59:59+01:00"
  }
}
```

#### Delete Token

```
DELETE /privacy-vault/tokens/{token}/
```

Response:
```json
{
  "status": "success",
  "data": {
    "message": "Token successfully deleted and associated data purged"
  }
}
```

### Synthetic Data Management (Demo Mode)

#### Generate Demo Data

```
POST /demo/generate/
```

Request:
```json
{
  "scope": ["assets", "bank_accounts", "transactions", "documents", "emails"],
  "volume": "medium", // Options: small, medium, large
  "time_range": {
    "start_date": "2020-01-01",
    "end_date": "2023-12-31"
  },
  "seed": 12345 // Optional, for reproducible data generation
}
```

Response:
```json
{
  "status": "success",
  "data": {
    "job_id": "gen_job_789xyz",
    "status": "processing",
    "estimated_completion_time": "2023-08-15T12:30:45+01:00",
    "items_to_generate": {
      "users": 5,
      "assets": 15,
      "bank_accounts": 8,
      "transactions": 1250,
      "documents": 45,
      "emails": 120
    }
  }
}
```

#### Check Demo Data Generation Status

```
GET /demo/status/{job_id}/
```

Response:
```json
{
  "status": "success",
  "data": {
    "job_id": "gen_job_789xyz",
    "status": "completed", // Options: processing, completed, failed
    "completed_at": "2023-08-15T12:28:30+01:00",
    "items_generated": {
      "users": 5,
      "assets": 15,
      "bank_accounts": 8,
      "transactions": 1250,
      "documents": 45,
      "emails": 120
    }
  }
}
```

#### Reset Demo Data

```
POST /demo/reset/
```

Request:
```json
{
  "scope": ["all"], // or specific entities ["assets", "bank_accounts", etc.]
  "confirmation": "RESET_DEMO_DATA"
}
```

Response:
```json
{
  "status": "success",
  "data": {
    "message": "Demo data has been reset successfully",
    "reset_entities": ["users", "assets", "bank_accounts", "transactions", "documents", "emails"]
  }
}
```

#### Toggle Demo Mode

```
POST /demo/toggle/
```

Request:
```json
{
  "demo_mode_enabled": true,
  "confirmation": "TOGGLE_DEMO_MODE"
}
```

Response:
```json
{
  "status": "success",
  "data": {
    "demo_mode_enabled": true,
    "applied_to_all_endpoints": true,
    "message": "System is now in demo mode. All API responses will use synthetic data."
  }
}
```

## Error Handling

### Common Error Codes

- `400 Bad Request`: Invalid request format or parameters
- `401 Unauthorized`: Authentication failure
- `403 Forbidden`: Permission denied
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Unexpected server error

### Validation Errors

For validation errors, the response includes detailed information:

```json
{
  "status": "error",
  "error": {
    "code": 422,
    "message": "Validation failed",
    "details": {
      "buying_price": ["This field is required"],
      "postal_code": ["Invalid postal code format"]
    }
  }
}
```

## Rate Limiting

To protect the database server resources:

- 100 requests per minute per IP address
- Rate limit headers included in responses:
  - `X-RateLimit-Limit`: Request limit
  - `X-RateLimit-Remaining`: Remaining requests
  - `X-RateLimit-Reset`: Time until limit resets (seconds)

When rate limit is exceeded:

```json
{
  "status": "error",
  "error": {
    "code": 429,
    "message": "Too many requests. Please try again in 45 seconds."
  }
}
```

## API Versioning

API versioning is managed through the URL path:
- Current version: `v1`
- When breaking changes are introduced, a new version will be created

## Batch Operations

For efficient processing, batch operations are supported:

```
POST /batch/
```

Request:
```json
{
  "operations": [
    {
      "method": "GET",
      "path": "/assets/1/"
    },
    {
      "method": "GET",
      "path": "/bank-accounts/3/"
    }
  ]
}
```

Response:
```json
{
  "status": "success",
  "data": [
    {
      "status": "success",
      "data": {
        // Asset 1 data
      }
    },
    {
      "status": "success",
      "data": {
        // Bank account 3 data
      }
    }
  ]
}
```

## Privacy Vault Special Considerations

### Access Purposes

When accessing the Privacy Vault, the `X-Purpose` header must be included with one of the following values:

- `display`: For showing data to authorized users in the UI
- `reporting`: For including data in reports and analytics
- `audit`: For security and compliance audit purposes
- `export`: For data export operations
- `integration`: For third-party service integration

### Token Formats

Privacy Vault tokens follow specific formats for different data types:

- Bank account details: `tkn_ba_[random string]`
- Personal identification: `tkn_pi_[random string]`
- Address information: `tkn_addr_[random string]`
- Financial records: `tkn_fin_[random string]`
- Tax information: `tkn_tax_[random string]`

### Token Lifetimes

Tokens have configurable lifetimes based on sensitivity:

- High sensitivity data: 30-day maximum token lifetime
- Medium sensitivity data: 90-day maximum token lifetime
- Low sensitivity data: 365-day maximum token lifetime

After expiration, tokens must be refreshed through an authenticated request.

## Cross-Cutting Concerns

### Pagination

List endpoints support pagination with the following parameters:
- `limit`: Number of items per page (default: 20, max: 100)
- `offset`: Number of items to skip

Response includes navigation links:
```json
{
  "count": 45,
  "next": "/api/v1/assets/?offset=20&limit=20",
  "previous": null,
  "results": [...]
}
```

### Filtering

Most list endpoints support filtering using query parameters.

### Sorting

Use the `sort` parameter to specify sorting field and direction:
- `sort=name`: Sort by name ascending
- `sort=-buying_date`: Sort by buying date descending (note the minus prefix)

### Field Selection

Use the `fields` parameter to request only specific fields:
```
GET /assets/?fields=id,nickname,address,buying_price
```

### Demo Mode Indicator

When operating in demo mode, all responses include:
- `is_demo_data: true` flag in the response data
- `X-Demo-Mode: true` header in the HTTP response

## Webhook Notifications

The API supports sending webhook notifications for data changes:

1. Register a webhook:
```
POST /webhooks/
```

Request:
```json
{
  "event_types": ["asset.created", "asset.updated", "reservation.created"],
  "target_url": "https://webhook-handler.example.com/callback",
  "secret": "your_webhook_secret"
}
```

2. Webhook payload format:
```json
{
  "event_type": "asset.created",
  "timestamp": "2023-06-15T08:45:30+01:00",
  "data": {
    // Resource data
  },
  "is_demo_data": false,
  "signature": "computed_hmac_signature"
}
``` 