# Administrative API

This module provides a RESTful API for managing administrative documents, insurance contracts, and files.

## Authentication

All endpoints require authentication. You can obtain an authentication token by making a POST request to:

```
POST /api-token-auth/
```

With the following payload:
```json
{
  "username": "your_username",
  "password": "your_password"
}
```

Then include the token in your requests:
```
Authorization: Token your_token_here
```

## API Endpoints

### Insurance Companies

- **List and Create Companies**
  - `GET/POST /api/administrative/insurance-companies/`
  - Filters: `name`, `phone_number`

- **Retrieve, Update, Delete Company**
  - `GET/PUT/PATCH/DELETE /api/administrative/insurance-companies/{id}/`

### Insurance Contracts

- **List and Create Contracts**
  - `GET/POST /api/administrative/insurance-contracts/`
  - Filters: `company`, `type`, `is_insurance_active`, `person`

- **Retrieve, Update, Delete Contract**
  - `GET/PUT/PATCH/DELETE /api/administrative/insurance-contracts/{id}/`

- **Get Files for Contract**
  - `GET /api/administrative/insurance-contracts/{id}/files/`

- **Upload File for Contract**
  - `POST /api/administrative/insurance-contracts/{id}/files/`
  - Form data: `name` (optional), `content` (required)

### Documents

- **List and Create Documents**
  - `GET/POST /api/administrative/documents/`
  - Filters: `user`, `type`

- **Retrieve, Update, Delete Document**
  - `GET/PUT/PATCH/DELETE /api/administrative/documents/{id}/`

- **Get Files for Document**
  - `GET /api/administrative/documents/{id}/files/`

- **Upload File for Document**
  - `POST /api/administrative/documents/{id}/files/`
  - Form data: `name` (optional), `content` (required)

### Files

- **List and Create Files**
  - `GET/POST /api/administrative/files/`
  - Filters: `name`

- **Retrieve, Update, Delete File**
  - `GET/PUT/PATCH/DELETE /api/administrative/files/{id}/`

## Example Requests

### Create an Insurance Company

```bash
curl -X POST \
  http://localhost:8000/api/administrative/insurance-companies/ \
  -H 'Authorization: Token your_token_here' \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Example Insurance Co",
    "phone_number": 5551234567,
    "site_app_company": "exampleinsurance.com"
}'
```

### Create an Insurance Contract

```bash
curl -X POST \
  http://localhost:8000/api/administrative/insurance-contracts/ \
  -H 'Authorization: Token your_token_here' \
  -H 'Content-Type: application/json' \
  -d '{
    "company": 1,
    "type": "Real Estate insurance",
    "real_estate_asset": 2,
    "contract_number": "INS-12345",
    "starting_date": "2023-01-01",
    "ending_date": "2024-01-01",
    "is_insurance_active": true,
    "personal_email_used": "user@example.com",
    "annual_price": {"2023": 400},
    "coverage": {"liability": "full coverage"}
}'
```

### Upload a Document File

```bash
curl -X POST \
  http://localhost:8000/api/administrative/documents/1/files/ \
  -H 'Authorization: Token your_token_here' \
  -H 'Content-Type: multipart/form-data' \
  -F 'name=Passport Scan' \
  -F 'content=@/path/to/your/file.pdf'
```

## Error Handling

API returns standard HTTP status codes:

- 200: OK
- 201: Created
- 204: No Content
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error

Error responses follow this format:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable error message",
    "details": {}
  }
}
``` 