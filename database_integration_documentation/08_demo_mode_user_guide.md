# Demo Mode User Guide

## Overview

This document provides instructions for using the Demo Mode feature in the Personal Database Assistant. Demo Mode allows users to interact with the system using synthetic data rather than real user data, making it ideal for demonstrations, training, and testing without exposing sensitive information.

## What is Demo Mode?

Demo Mode is a special operating state of the Personal Database Assistant that:

1. Uses completely synthetic (fake) data instead of real user data
2. Provides a realistic experience of all system features
3. Is clearly marked throughout the interface to prevent confusion
4. Allows safe demonstrations to stakeholders and new users
5. Facilitates training without privacy risks

## Benefits of Using Demo Mode

- **Privacy Protection**: Demonstrate system capabilities without exposing real user data
- **Consistent Experience**: Predictable data patterns for reliable demonstrations
- **Comprehensive Examples**: Pre-populated with examples covering all system features
- **Safe Experimentation**: Test features without risk to production data
- **Training Environment**: Train new users without access to sensitive information

## Activating Demo Mode

### Via Web Interface

1. Log in to the Personal Database Assistant
2. Navigate to **Settings** > **System Preferences**
3. Locate the **Demo Mode** section
4. Toggle the **Enable Demo Mode** switch to ON
5. Select a synthetic dataset from the dropdown (if multiple are available)
6. Click **Apply Changes**

![Demo Mode Activation](demo_mode_activation.png)

### Via API

```javascript
// Example: Enable Demo Mode via API
async function enableDemoMode() {
  const response = await fetch('https://api.personaldb.example/system/demo-mode', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${await getAuthToken()}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      enabled: true,
      dataset_id: 'latest', // or a specific version
      duration: '24h' // optional time limit
    })
  });
  
  return response.json();
}
```

### Administrator-Enforced Demo Mode

Administrators can enforce Demo Mode for specific user accounts:

1. Log in with administrator credentials
2. Navigate to **Admin** > **User Management**
3. Select the target user account
4. In the **Permissions** tab, enable **Force Demo Mode**
5. Choose the appropriate synthetic dataset
6. Set an optional expiration date/time
7. Click **Save Changes**

## Demo Mode Indicators

When Demo Mode is active, the system provides clear visual indicators:

1. **Demo Banner**: A prominent banner appears at the top of all pages
2. **Color Theme**: The interface uses a distinct color scheme (default: blue)
3. **Data Badges**: All synthetic data entries are marked with a "DEMO" badge
4. **Export Watermarks**: Any exported reports include "DEMO DATA" watermarks
5. **API Response Headers**: All API responses include a `X-Demo-Mode: true` header

![Demo Mode Indicators](demo_mode_indicators.png)

## Working with Synthetic Data

### Data Characteristics

The synthetic data provided in Demo Mode:

1. Is clearly marked with identifiers (e.g., usernames prefixed with "demo_")
2. Follows realistic patterns but contains no actual user information
3. Includes examples of all supported entity types and relationships
4. Contains pre-defined scenarios for demonstrations

### Available Synthetic Data Sets

The system includes several synthetic datasets for different purposes:

| Dataset Name | Description | Best For |
|--------------|-------------|----------|
| Standard | General-purpose dataset with moderate volume | General demonstrations |
| Financial | Enhanced financial data with complex transactions | Financial feature demos |
| Real Estate | Focus on property assets and management | Real estate investment demos |
| Large Volume | High volume data for performance testing | Performance demonstrations |
| Edge Cases | Data with unusual patterns and edge cases | Testing error handling |

To switch between datasets:

1. Navigate to **Settings** > **Demo Preferences**
2. Select the desired dataset from the **Active Dataset** dropdown
3. Click **Apply**

### Demo Scenarios

The synthetic data is organized into predefined scenarios for effective demonstrations:

#### 1. Real Estate Investment Portfolio

A collection of properties with rental income, expenses, and financial performance metrics.

**Key Features to Demonstrate:**
- Property management dashboard
- Rental income tracking
- Expense categorization
- ROI calculations

**Sample Flow:**
1. Navigate to **Assets** > **Real Estate**
2. Select "Demo Beach House"
3. Review property details and financial summary
4. Explore the "Rental History" tab
5. Generate a "Property Performance Report"

#### 2. Personal Finance Management

A comprehensive personal finance setup with multiple accounts, budgets, and financial goals.

**Key Features to Demonstrate:**
- Multi-account dashboard
- Budget tracking
- Spending analysis
- Financial goal progress

**Sample Flow:**
1. Navigate to **Finances** > **Dashboard**
2. Review account balances and recent transactions
3. Open the "Monthly Budget" report
4. Demonstrate the "Spending Categories" visualization
5. Show progress on "Vacation Fund" savings goal

#### 3. Document Management

A collection of financial and legal documents with metadata and search capabilities.

**Key Features to Demonstrate:**
- Document upload and categorization
- Metadata extraction
- Full-text search
- Document relationships

**Sample Flow:**
1. Navigate to **Documents** > **All Documents**
2. Filter by "Property" documents
3. Open "Demo Beach House Purchase Agreement"
4. Show extracted metadata and related documents
5. Demonstrate search functionality with term "insurance"

## Demo Mode Limitations

While Demo Mode provides a comprehensive system experience, there are some limitations:

1. **External Integrations**: Some third-party integrations may be simulated or unavailable
2. **Email Notifications**: Emails are logged but not actually sent externally
3. **Data Persistence**: Changes to synthetic data may be reset periodically
4. **Performance Characteristics**: May not exactly match production environment
5. **Custom Data**: Cannot import custom data while in Demo Mode

## Demo Mode for Developers

### Testing with Synthetic Data

For developers, Demo Mode provides a controlled environment for testing:

1. **API Testing**: All APIs work with synthetic data when Demo Mode is active
2. **Integration Testing**: Test integrations without affecting production data
3. **UI Development**: Develop UI components against consistent datasets
4. **Performance Testing**: Test with various data volumes

### Demo Mode API Headers

When making API calls in Demo Mode:

1. **Request Header**: Include `X-Demo-Mode: true` in your requests
2. **Response Verification**: Check for `X-Using-Synthetic-Data: true` in responses

### Generating Custom Synthetic Datasets

Administrators and developers can generate custom synthetic datasets:

1. Navigate to **Admin** > **Demo Data** > **Generate Dataset**
2. Configure generation parameters:
   - Entity types to include
   - Data volume
   - Time ranges
   - Special case scenarios
3. Click **Generate Dataset**
4. Once complete, the new dataset becomes available for selection

```javascript
// Example: Generate a custom synthetic dataset via API
async function generateCustomDataset() {
  const response = await fetch('https://api.personaldb.example/admin/synthetic/generate', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${await getAdminToken()}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      name: 'Custom Test Dataset',
      description: 'Dataset for API feature testing',
      parameters: {
        entity_types: ['users', 'assets', 'transactions', 'documents'],
        volume: 'medium',
        date_range: {
          start: '2021-01-01',
          end: '2023-12-31'
        },
        special_cases: ['missing_data', 'high_value_transactions']
      }
    })
  });
  
  return response.json();
}
```

## Demo Mode for Training

### Structured Training Environments

Demo Mode is ideal for training new users:

1. **Guided Tours**: Follow predefined scenarios to learn system features
2. **Safe Practice**: Make changes without affecting real data
3. **Reset Capability**: Return to initial state after practice sessions
4. **Role-Specific Examples**: Data relevant to different user roles

### Training Mode vs. Standard Demo Mode

The system offers a special Training variation of Demo Mode:

| Feature | Standard Demo Mode | Training Mode |
|---------|-------------------|---------------|
| Data Reset | Periodic/scheduled | On-demand by user |
| Guidance | None | Step-by-step instructions |
| Progress Tracking | No | Yes, with completion metrics |
| Error Forgiveness | Standard validation | Enhanced help on errors |
| Complexity | Full system complexity | Gradual feature introduction |

To activate Training Mode:

1. Enable Demo Mode as described earlier
2. Navigate to **Help** > **Training Center**
3. Select **Start Guided Training**
4. Choose a training module from the available options

## Best Practices for Demonstrations

When using Demo Mode for presentations or demonstrations:

1. **Prepare in Advance**
   - Familiarize yourself with the synthetic data scenarios
   - Prepare a demonstration script covering key features
   - Test your demonstration flow beforehand
   - Bookmark important pages for quick access

2. **Clear Communication**
   - Explicitly mention that you are using Demo Mode
   - Explain that all data is synthetic and not real user data
   - Point out the Demo Mode indicators
   - Set expectations about feature availability

3. **Effective Showcasing**
   - Focus on one feature at a time
   - Use the predefined scenarios that best highlight each feature
   - Show both the dashboard/summary views and detailed information
   - Demonstrate how data flows between different system components

4. **Handling Questions**
   - Prepare for common questions about data privacy
   - Know how to quickly find specific examples in the synthetic data
   - Be ready to explain the differences between Demo Mode and Production
   - Understand how to demonstrate specific use cases on request

## Troubleshooting Demo Mode

### Common Issues and Solutions

| Issue | Possible Cause | Solution |
|-------|---------------|----------|
| Demo Mode won't activate | Insufficient permissions | Request Demo Mode access from administrator |
| Missing synthetic data | Dataset loading incomplete | Wait for completion or select a different dataset |
| Inconsistent data | Data corruption or generation error | Reset the synthetic dataset |
| Slow performance | Large synthetic dataset | Switch to a smaller volume dataset |
| Feature unavailable | Not supported in Demo Mode | Check documentation for Demo Mode limitations |

### Resetting Synthetic Data

To reset the synthetic data to its original state:

1. Navigate to **Settings** > **Demo Preferences**
2. Click the **Reset Synthetic Data** button
3. Confirm the reset when prompted

### Reporting Issues

If you encounter problems with Demo Mode:

1. Navigate to **Help** > **Support**
2. Click **Report an Issue**
3. Select **Demo Mode Problem** from the category dropdown
4. Provide detailed information about the issue
5. Include screenshots if possible
6. Submit the report

## Exiting Demo Mode

To return to normal operation with real data:

1. Navigate to **Settings** > **System Preferences**
2. Locate the **Demo Mode** section
3. Toggle the **Enable Demo Mode** switch to OFF
4. Click **Apply Changes**
5. Confirm the switch when prompted

**Important**: All changes made to synthetic data will be discarded when exiting Demo Mode.

## Security Considerations

Even when using synthetic data, maintain good security practices:

1. **Access Control**: Only authorized users should access Demo Mode
2. **Demo Data Export**: Clearly mark any exported demo data
3. **Session Management**: Log out when demonstrations are complete
4. **Feature Limitations**: Some administrative functions may be restricted
5. **Screenshot Awareness**: Screenshots of Demo Mode should include visible indicators

## Appendix: Demo Data Examples

### Sample User Profiles

| Username | Email | Role | Description |
|----------|-------|------|-------------|
| demo_john | john.smith@example.com | Standard User | General personal finance management |
| demo_investor | real.estate@example.com | Property Investor | Multiple real estate investments |
| demo_family | family.finance@example.com | Family Account | Joint finances management |
| demo_business | small.business@example.com | Business User | Small business financial tracking |

### Sample Assets

| Name | Type | Value | Description |
|------|------|-------|-------------|
| Demo Beach House | Real Estate | $450,000 | Vacation rental property with income |
| Demo City Apartment | Real Estate | $320,000 | Residential rental unit |
| Demo Investment Portfolio | Financial | $250,000 | Diverse stock and bond holdings |
| Demo Luxury Vehicle | Vehicle | $75,000 | Depreciating asset example |

### Sample Financial Accounts

| Name | Type | Balance | Institution |
|------|------|---------|-------------|
| Demo Checking Account | Checking | $8,500 | Demo National Bank |
| Demo Savings Account | Savings | $45,000 | Demo Credit Union |
| Demo Investment Account | Investment | $250,000 | Demo Investments Inc. |
| Demo Credit Card | Credit | -$3,200 | Demo Card Services |

## Appendix: Demo Mode API Reference

### Key Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/system/demo-mode` | GET | Check current Demo Mode status |
| `/system/demo-mode` | POST | Enable or disable Demo Mode |
| `/system/demo-mode/datasets` | GET | List available synthetic datasets |
| `/system/demo-mode/reset` | POST | Reset synthetic data to initial state |
| `/system/demo-mode/train` | POST | Activate Training Mode variation |

### Sample Responses

#### Demo Mode Status

```json
GET /system/demo-mode
{
  "enabled": true,
  "dataset": {
    "id": "standard-2023-v2",
    "name": "Standard Dataset 2023",
    "version": 2,
    "created_at": "2023-05-15T10:30:00Z",
    "entity_counts": {
      "users": 10,
      "assets": 35,
      "accounts": 25,
      "transactions": 3500,
      "documents": 150
    }
  },
  "activated_at": "2023-08-10T14:22:15Z",
  "activated_by": "admin_user",
  "expires_at": null
}
```

#### Available Datasets

```json
GET /system/demo-mode/datasets
{
  "datasets": [
    {
      "id": "standard-2023-v2",
      "name": "Standard Dataset 2023",
      "description": "General purpose demonstration data",
      "version": 2,
      "size": "medium",
      "created_at": "2023-05-15T10:30:00Z"
    },
    {
      "id": "financial-2023-v1",
      "name": "Financial Focus Dataset",
      "description": "Enhanced financial transaction data",
      "version": 1,
      "size": "medium",
      "created_at": "2023-06-22T08:15:00Z"
    },
    {
      "id": "large-volume-2023-v1",
      "name": "Large Volume Dataset",
      "description": "High volume data for performance testing",
      "version": 1,
      "size": "large",
      "created_at": "2023-07-05T16:45:00Z"
    }
  ]
}
``` 