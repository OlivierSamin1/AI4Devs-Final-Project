# User Guide

This guide provides comprehensive instructions for using the Personal Asset Management System. It covers navigation, data entry, and common tasks.

## Table of Contents

1. [Getting Started](#getting-started)
2. [System Navigation](#system-navigation)
3. [Administrative Tasks](#administrative-tasks)
4. [Financial Management](#financial-management)
5. [Real Estate Management](#real-estate-management)
6. [Transportation Management](#transportation-management)
7. [Health Management](#health-management)
8. [Tax Management](#tax-management)
9. [Insurance Management](#insurance-management)
10. [Document Management](#document-management)
11. [Reporting](#reporting)
12. [Tips and Best Practices](#tips-and-best-practices)

## Getting Started

### Accessing the System

1. Open your web browser and navigate to the system URL (e.g., `http://localhost:8000` or your custom domain)
2. Log in with your username and password
3. For first-time login, use the credentials provided by your system administrator

### Dashboard Overview

After logging in, you'll see the admin dashboard with navigation links to all system modules. The dashboard includes:

- Quick links to common tasks
- Overview of your assets
- Recent activity summary
- Navigation menu for all modules

## System Navigation

### Main Menu

The main menu is divided into sections corresponding to the system's modules:

- **Administrative**: User and document management
- **Financial**: Banking and financial records
- **Real Estate**: Property and rental management
- **Transportation**: Vehicle management
- **Health**: Medical records and health products
- **Tax**: Tax records and management
- **Insurance**: Insurance policy management

### Search Functionality

Use the search bar at the top of any page to quickly find records:

1. Enter keywords (e.g., property address, account number)
2. Select the entity type from the dropdown (optional)
3. Click the search icon or press Enter

### Filtering and Sorting

On list views, you can filter and sort records:

1. Look for filter options in the right sidebar
2. Click column headers to sort by that column
3. Use the "Advanced Filter" option for complex filtering

## Administrative Tasks

### User Management

#### Adding a New User

1. Navigate to "Authentication and Authorization" > "Users"
2. Click "Add User" in the top right corner
3. Enter the required information (username, password)
4. Click "Save and continue editing"
5. Set additional user details and permissions
6. Click "Save"

#### Managing Permissions

1. Navigate to "Authentication and Authorization" > "Users"
2. Select the user you want to modify
3. In the "Permissions" section, assign appropriate user permissions
4. Click "Save"

### Document Management

#### Adding a New Document

1. Navigate to "Administrative" > "Documents"
2. Click "Add Document" in the top right corner
3. Fill in the document details (name, type)
4. Associate the document with a user if applicable
5. Add comments if needed
6. Click "Save"
7. After saving, you can attach files to the document

## Financial Management

### Bank Management

#### Adding a New Bank

1. Navigate to "Financial" > "Banks"
2. Click "Add Bank" in the top right corner
3. Enter the bank details (name, address, etc.)
4. Click "Save"

### Bank Account Management

#### Adding a New Bank Account

1. Navigate to "Financial" > "Bank Accounts"
2. Click "Add Bank Account" in the top right corner
3. Select the bank from the dropdown
4. Select the account holder (titular)
5. Enter the account details (name, IBAN, BIC, etc.)
6. Set the starting date and status
7. Click "Save"
8. After saving, you can add related bank cards

#### Recording Year-End Balances

1. Navigate to "Financial" > "Bank Accounts"
2. Select the account you want to update
3. Scroll to the "Value on 31_12" field
4. Enter the JSON data in the format: `{"2023": 10000, "2022": 9500}`
5. Click "Save"

### Bank Card Management

#### Adding a New Bank Card

1. Navigate to "Financial" > "Bank Cards"
2. Click "Add Bank Card" in the top right corner
3. Select the associated bank account
4. Enter the card details (name, number, expiration date)
5. Set the card status (active/inactive)
6. Click "Save"

## Real Estate Management

### Property Management

#### Adding a New Property

1. Navigate to "Real Estate" > "Assets"
2. Click "Add Asset" in the top right corner
3. Enter the property details (nickname, address, etc.)
4. Select the owner from the dropdown
5. Enter purchase information (date, price)
6. Set property status (mortgage, rental, primary residence)
7. Click "Save"
8. After saving, you can associate bank accounts, contracts, and upload files

### Mortgage Management

#### Recording a New Mortgage

1. Navigate to "Real Estate" > "Mortgages"
2. Click "Add Mortgage" in the top right corner
3. Select the associated property
4. Enter mortgage details (name, bank account, dates)
5. Record financial information (rates, annual interests, capital)
6. Click "Save"

### Rental Management

#### Setting Up a Rental Contract

1. Navigate to "Real Estate" > "Renting Management Contracts"
2. Click "Add Renting Management Contract" in the top right corner
3. Select or create the management company
4. Select the property being managed
5. Enter contract details (number, dates, status)
6. Click "Save"

#### Managing Tenants

1. Navigate to "Real Estate" > "Tenants"
2. Click "Add Tenant" in the top right corner
3. Select the associated property
4. Enter tenant details (name, contact information, ID)
5. Enter rental contract information (dates, deposit amount)
6. Set tenant status (current/former)
7. Click "Save"

### Utility Management

#### Adding a Utility Contract

1. Navigate to "Real Estate" > "Utility Contracts"
2. Click "Add Utility Contract" in the top right corner
3. Select the utility supplier (or create a new one)
4. Select the user and property
5. Choose the service type (electricity, water, etc.)
6. Enter contract details (number, dates, status)
7. Enter payment information (monthly amounts)
8. Click "Save"

## Transportation Management

### Vehicle Management

#### Adding a New Vehicle

1. Navigate to "Transportation" > "Assets"
2. Click "Add Asset" in the top right corner
3. Select the owner from the dropdown
4. Enter vehicle details (type, brand, model, registration)
5. Enter purchase information (date, price, condition)
6. Set vehicle status (credit, leasing, inspections)
7. Add any additional comments
8. Click "Save"
9. After saving, you can upload related documents

## Health Management

### Medical Bill Management

#### Recording a Medical Bill

1. Navigate to "Health" > "Bills"
2. Click "Add Bill" in the top right corner
3. Enter the healthcare provider's name
4. Select the client (patient)
5. Enter bill details (name, date, amount)
6. Set payment status
7. Click "Save"
8. After saving, you can upload bill documents

### Health Product Management

#### Adding a Health Product

1. Navigate to "Health" > "Products"
2. Click "Add Product" in the top right corner
3. Enter product details (name, composition, benefits)
4. Set product properties (natural, age restrictions)
5. Enter information source and date
6. Add any comments
7. Click "Save"
8. After saving, you can associate the product with symptoms

## Tax Management

### Tax Record Management

#### Recording a Tax Payment

1. Navigate to "Tax" > "Taxes"
2. Click "Add Tax" in the top right corner
3. Enter tax details (name, type, year)
4. Associate the tax with the appropriate entity (property, vehicle, person)
5. Set management company information if applicable
6. Enter payment amount
7. Click "Save"
8. After saving, you can upload tax documents

## Insurance Management

### Insurance Policy Management

#### Adding an Insurance Policy

1. Navigate to "Insurance" > "Insurance Contracts"
2. Click "Add Insurance Contract" in the top right corner
3. Select the insurance company (or create a new one)
4. Select the insurance type (Real Estate, Transportation, Person)
5. Select the associated entity based on the type
6. Enter contract details (number, dates, status)
7. Enter coverage and premium information
8. Click "Save"
9. After saving, you can upload policy documents

## Document Management

### Uploading Files

File upload is available in various parts of the system. The general process is:

1. First, save the parent record (e.g., property, account, vehicle)
2. In the edit view of the parent record, find the "Files" section
3. Click "Add another [file type]" button
4. Click "Choose File" to select a file from your computer
5. Enter a name for the file (optional)
6. Click "Save" to upload the file

### Viewing and Managing Files

1. Navigate to the parent record that contains the files
2. Files are displayed in the "Files" section
3. Click on the file link to view or download it
4. Use the edit or delete icons to modify or remove files

## Reporting

The system provides various reporting options through the Django admin interface:

### Filtering and Exporting Data

1. Navigate to the relevant section (e.g., "Real Estate" > "Assets")
2. Use the filter options in the right sidebar to narrow down records
3. Select records using the checkboxes
4. Use the "Action" dropdown to export selected data

### Financial Reporting

Financial data is stored in JSON fields for year-by-year tracking. View this data by:

1. Navigate to the relevant section (e.g., "Bank Accounts")
2. Select the specific record
3. JSON fields like "value_on_31_12" show year-by-year financial information

## Tips and Best Practices

### Data Organization

- Use consistent naming conventions for all records
- Keep documentation up-to-date
- Regularly review and update financial information
- Use the comment fields to store additional context

### Optimal System Use

- Upload documents as soon as they are received
- Record financial transactions promptly
- Regularly back up your database
- Review tax-deductible expenses before tax season

### Security Best Practices

- Use strong, unique passwords
- Do not share your login credentials
- Log out when not using the system
- Regularly update your contact information

For technical assistance or feature requests, contact your system administrator. 