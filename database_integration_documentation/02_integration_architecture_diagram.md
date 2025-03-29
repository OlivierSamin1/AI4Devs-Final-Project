# Integration Architecture Diagram

## Overview

This document illustrates the architecture and data flows for the Personal Database Assistant system, which connects an offline database (Raspberry Pi 3B) with an internet-accessible web application (Raspberry Pi 4).

## System Components

### High-Level Component Diagram

```mermaid
graph TB
    subgraph Internet
        User[User Browser]
        ExternalServices[External Services]
    end
    
    subgraph "DMZ (Internet-Facing)"
        RPi4[Raspberry Pi 4\nWeb Server]
        style RPi4 fill:#9cf,stroke:#333,stroke-width:2px
        
        subgraph "Web Server Components"
            WebApp[Django Web Application]
            APIClient[API Client Service]
            Auth[Authentication Layer]
            DocProcessor[Document Processing]
            AIService[AI Integration Service]
            EmailInt[Email Integration]
            Redis[Redis Cache/Queue]
            DemoManager[Demo Data Manager]
            DataAccessLayer[Data Access Layer]
        end
    end
    
    subgraph "Secure Local Network"
        RPi3B[Raspberry Pi 3B\nDatabase Server]
        style RPi3B fill:#fcf,stroke:#333,stroke-width:2px
        
        subgraph "Database Server Components"
            Django[Django REST API]
            PostgreSQL[PostgreSQL Database]
            FileStorage[File Storage]
            Backup[Backup Service]
            PrivacyVault[Data Privacy Vault]
            SyntheticData[Synthetic Data Store]
        end
    end
    
    User <--> |HTTPS| RPi4
    ExternalServices <--> |HTTPS| RPi4
    
    WebApp --> Auth
    WebApp --> APIClient
    WebApp --> DocProcessor
    WebApp --> AIService
    WebApp --> EmailInt
    WebApp --> DemoManager
    DemoManager <-.-> DataAccessLayer
    DataAccessLayer --> APIClient
    DocProcessor --> Redis
    APIClient --> Redis
    
    RPi4 <--> |Secure API| RPi3B
    
    Django --> PostgreSQL
    Django --> FileStorage
    Django --> PrivacyVault
    Django --> SyntheticData
    PostgreSQL --> Backup
    PrivacyVault --> Backup
    
    class RPi4,RPi3B emphasize;
```

## Network Architecture

```mermaid
graph TB
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
            Demo[Synthetic Data]
        end
    end
    
    User --> |HTTPS:443| Router
    AI <--> |HTTPS| RPi4
    Gmail <--> |HTTPS| RPi4
    
    Router --> |Port Forward\nHTTPS:443| RPi4
    RPi4 <--> |Internal API\nHTTP:8000| RPi3B
    RPi3B <--> DPV
    RPi3B <--> Demo
    
    style Router fill:#f96,stroke:#333,stroke-width:2px
    style RPi4 fill:#9cf,stroke:#333,stroke-width:2px
    style RPi3B fill:#fcf,stroke:#333,stroke-width:2px
    style DPV fill:#fcf,stroke:#333,stroke-width:2px
    style Demo fill:#dfd,stroke:#333,stroke-width:2px
```

## Data Flow

### Authentication Process

```mermaid
sequenceDiagram
    participant User as User Browser
    participant RPi4 as Raspberry Pi 4 (Web Server)
    participant Auth as Authentication Layer
    participant RPi3B as Raspberry Pi 3B (Database)
    
    User->>RPi4: HTTPS Request with Credentials
    RPi4->>Auth: Validate User Credentials
    Auth-->>RPi4: Authentication Token
    RPi4->>User: Set Session Cookie
    
    User->>RPi4: Request Data with Session Cookie
    RPi4->>Auth: Validate Session
    Auth-->>RPi4: Session Valid
    RPi4->>RPi3B: API Request with API Key
    RPi3B-->>RPi4: Data Response
    RPi4-->>User: Formatted Data Response
```

### Data Query Flow

```mermaid
sequenceDiagram
    participant User as User Browser
    participant WebApp as Web Application (RPi4)
    participant DataAccess as Data Access Layer (RPi4)
    participant Cache as Redis Cache (RPi4)
    participant API as API Client (RPi4)
    participant DB as Database API (RPi3B)
    participant DPV as Data Privacy Vault (RPi3B)
    participant Demo as Synthetic Data (RPi3B)
    
    User->>WebApp: Request Data (e.g., Asset Information)
    WebApp->>DataAccess: Request Data
    
    alt Demo Mode ON
        DataAccess->>Demo: Request Synthetic Data
        Demo-->>DataAccess: Return Demo Data
    else Demo Mode OFF
        DataAccess->>Cache: Check Cache for Data
        
        alt Data in Cache
            Cache-->>DataAccess: Return Cached Data
        else Data Not in Cache
            DataAccess->>API: Request Data from API
            API->>DB: Send API Request
            
            alt Contains Sensitive Data
                DB->>DPV: Request Tokenized Data
                DPV-->>DB: Return Tokens or Data Based on Access Policy
            end
            
            DB-->>API: Return Raw Data
            API->>Cache: Store in Cache
            API-->>DataAccess: Return Processed Data
        end
    end
    
    DataAccess-->>WebApp: Return Data (Real or Demo)
    WebApp-->>User: Display Formatted Data
```

### Document Processing Flow

```mermaid
sequenceDiagram
    participant User as User Browser
    participant WebApp as Web Application (RPi4)
    participant DocProc as Document Processor (RPi4)
    participant AI as AI Service
    participant Queue as Redis Queue (RPi4)
    participant API as API Client (RPi4)
    participant DB as Database API (RPi3B)
    participant DPV as Data Privacy Vault (RPi3B)
    
    User->>WebApp: Upload Document
    WebApp->>DocProc: Process Document
    DocProc->>Queue: Queue for Processing
    
    loop Process Documents
        Queue-->>DocProc: Get Next Document
        DocProc->>AI: Extract Text & Metadata
        AI-->>DocProc: Return Extracted Data
        
        alt Contains Sensitive Data
            DocProc->>API: Request Tokenization
            API->>DPV: Tokenize Sensitive Data
            DPV-->>API: Return Token References
            API-->>DocProc: Return Tokens
        end
        
        DocProc->>API: Store Document & Metadata
        API->>DB: Save to Database
        DB-->>API: Confirmation
    end
    
    WebApp-->>User: Document Processing Confirmation
```

### Synthetic Data Generation Flow

```mermaid
sequenceDiagram
    participant Admin as Administrator
    participant WebApp as Web Application (RPi4)
    participant DemoMgr as Demo Data Manager (RPi4)
    participant API as API Client (RPi4)
    participant DB as Database API (RPi3B)
    participant SynData as Synthetic Data Generator (RPi3B)
    participant Store as Demo Data Store (RPi3B)
    
    Admin->>WebApp: Request Demo Data Generation
    WebApp->>DemoMgr: Initialize Generation Job
    DemoMgr->>API: Submit Generation Request
    API->>DB: Forward Generation Request
    DB->>SynData: Start Generation Process
    
    loop Generate Data Categories
        SynData->>SynData: Generate User Data
        SynData->>SynData: Generate Asset Data
        SynData->>SynData: Generate Financial Data
        SynData->>SynData: Generate Documents
        SynData->>SynData: Generate Email Data
    end
    
    SynData->>Store: Save Synthetic Data
    Store-->>SynData: Confirmation
    SynData-->>DB: Generation Complete
    DB-->>API: Job Status Update
    API-->>DemoMgr: Generation Completed
    DemoMgr-->>WebApp: Update Job Status
    WebApp-->>Admin: Demo Data Ready Notification
```

### Gmail Integration Flow

```mermaid
sequenceDiagram
    participant User as User Browser
    participant WebApp as Web Application (RPi4)
    participant EmailSvc as Email Service (RPi4)
    participant Gmail as Gmail API
    participant Queue as Redis Queue (RPi4)
    participant API as API Client (RPi4)
    participant DB as Database API (RPi3B)
    participant DPV as Data Privacy Vault (RPi3B)
    
    User->>WebApp: Request Gmail Integration
    WebApp->>EmailSvc: Authorize Gmail Access
    EmailSvc->>Gmail: Request Authorization
    Gmail-->>User: Authorization Consent Screen
    User->>Gmail: Grant Permission
    Gmail-->>EmailSvc: Authorization Token
    
    loop Sync Emails
        EmailSvc->>Gmail: Fetch Email Metadata
        Gmail-->>EmailSvc: Return Metadata
        EmailSvc->>Queue: Queue for Processing
        
        Queue-->>EmailSvc: Process Email Batch
        
        alt Contains Sensitive Information
            EmailSvc->>API: Request Tokenization
            API->>DPV: Tokenize Sensitive Data
            DPV-->>API: Return Tokens
            API-->>EmailSvc: Return Token References
        end
        
        EmailSvc->>API: Store Email Metadata
        API->>DB: Save to Database
        DB-->>API: Confirmation
    end
    
    WebApp-->>User: Gmail Sync Complete
```

## Data Privacy Vault Architecture

```mermaid
graph TD
    DB[PostgreSQL Database] -->|References| DPV[Data Privacy Vault]
    
    subgraph "Data Privacy Vault"
        APILayer[Privacy API Layer]
        AuthZ[Access Authorization]
        TokenMgr[Token Manager]
        CryptoSvc[Cryptography Service]
        AuditLog[Audit Logging]
        KeyMgmt[Key Management]
        Storage[Encrypted Storage]
    end
    
    DPV --> APILayer
    APILayer --> AuthZ
    AuthZ --> TokenMgr
    TokenMgr --> CryptoSvc
    CryptoSvc --> Storage
    APILayer --> AuditLog
    CryptoSvc --> KeyMgmt
    
    style DPV fill:#fcf,stroke:#333,stroke-width:2px
```

### Data Privacy Tokenization Flow

```mermaid
sequenceDiagram
    participant App as Application
    participant API as Privacy Vault API
    participant Auth as Access Authorization
    participant Token as Token Manager
    participant Crypto as Cryptography Service
    participant Store as Encrypted Storage
    participant Audit as Audit Logging
    
    App->>API: Store Sensitive Data
    API->>Auth: Validate Access Rights
    Auth-->>API: Access Granted
    API->>Token: Generate Token
    Token->>Crypto: Encrypt Data
    Crypto->>Store: Store Encrypted Data
    Store-->>Crypto: Storage Confirmation
    Crypto-->>Token: Store Token Mapping
    Token-->>API: Return Token Reference
    API->>Audit: Log Access
    API-->>App: Return Token
    
    App->>API: Retrieve Data Using Token
    API->>Auth: Validate Access Rights & Purpose
    Auth-->>API: Access Granted
    API->>Token: Resolve Token
    Token->>Crypto: Request Decryption
    Crypto->>Store: Retrieve Encrypted Data
    Store-->>Crypto: Return Encrypted Data
    Crypto-->>Token: Return Decrypted Data
    Token-->>API: Return Data
    API->>Audit: Log Access
    API-->>App: Return Sensitive Data
```

## Security Architecture

```mermaid
graph TD
    subgraph "Internet Zone"
        User[User Browser]
        ExtServices[External Services]
    end
    
    subgraph "Security Layers"
        SSL[SSL/TLS Encryption]
        FW[Router Firewall]
        WAF[Web Application Firewall]
        IPRestrict[IP Restriction]
        AuthN[Authentication]
        AuthZ[Authorization]
        APIKey[API Key Validation]
        CSRF[CSRF Protection]
        RateLimit[Rate Limiting]
        DPVSec[Data Privacy Controls]
    end
    
    subgraph "Network Zones"
        DMZ[DMZ Network\nRaspberry Pi 4]
        SecureZone[Secure Network\nRaspberry Pi 3B]
    end
    
    User --> SSL
    ExtServices --> SSL
    
    SSL --> FW
    FW --> WAF
    WAF --> DMZ
    
    DMZ --> IPRestrict
    IPRestrict --> APIKey
    APIKey --> SecureZone
    
    User --> AuthN
    AuthN --> AuthZ
    AuthZ --> DMZ
    
    DMZ --> CSRF
    DMZ --> RateLimit
    
    SecureZone --> DPVSec
    
    style DMZ fill:#9cf,stroke:#333,stroke-width:2px
    style SecureZone fill:#fcf,stroke:#333,stroke-width:2px
    style User fill:#fff,stroke:#333,stroke-width:1px
    style ExtServices fill:#fff,stroke:#333,stroke-width:1px
    style DPVSec fill:#fcf,stroke:#333,stroke-width:2px
```

## Demo Mode Architecture

```mermaid
graph TD
    subgraph "Web Application (RPi4)"
        UI[User Interface]
        DemoToggle[Demo Mode Toggle]
        APICalls[API Client Calls]
    end
    
    subgraph "Database Server (RPi3B)"
        API[Database API]
        DataRouter[Data Router]
        RealDB[Production Database]
        DemoDB[Synthetic Demo Database]
        Generator[Data Generator]
    end
    
    UI --> DemoToggle
    DemoToggle --> APICalls
    APICalls --> API
    API --> DataRouter
    
    DataRouter -->|Demo OFF| RealDB
    DataRouter -->|Demo ON| DemoDB
    
    Generator --> DemoDB
    
    style DemoToggle fill:#dfd,stroke:#333,stroke-width:2px
    style DemoDB fill:#dfd,stroke:#333,stroke-width:2px
    style Generator fill:#dfd,stroke:#333,stroke-width:2px
```

## Component Details

### Raspberry Pi 4 (Web Server)

- **Web Application**: Django-based web application with React frontend
- **API Client Service**: Handles communication with the database server
- **Document Processing**: OCR and document classification pipeline
- **AI Integration**: Interfaces with OpenAI/Hugging Face for natural language processing
- **Email Integration**: Connects to Gmail API for email retrieval and indexing
- **Redis**: Provides caching, message queue, and session storage
- **Authentication Layer**: JWT-based authentication system
- **Demo Data Manager**: Controls synthetic data generation and demo mode functionality
- **Data Access Layer**: Abstracts data source selection (real vs. demo data)

### Raspberry Pi 3B (Database Server)

- **Django REST API**: Provides secure API endpoints for the web server
- **PostgreSQL Database**: Stores all system data
- **File Storage**: Manages document files and attachments
- **Backup Service**: Handles regular database and file backups
- **Data Privacy Vault**: Secures sensitive personal information through tokenization
- **Synthetic Data Store**: Houses generated demo data separate from production data

## Data Privacy Vault Components

1. **Privacy API Layer**: Provides controlled access to sensitive data
2. **Access Authorization**: Enforces purpose-based access controls
3. **Token Manager**: Handles token generation and resolution
4. **Cryptography Service**: Manages encryption/decryption operations
5. **Encrypted Storage**: Secure database for sensitive information
6. **Audit Logging**: Records all access attempts and operations
7. **Key Management**: Handles encryption key rotation and security

## Synthetic Data Generation Components

1. **Data Generator**: Creates realistic synthetic data
2. **Generation Templates**: Defines data structure and relationships
3. **Demo Database**: Separate storage for synthetic data
4. **Demo Mode Toggle**: UI controls to switch between real and demo data
5. **Visual Indicators**: Clear UI markers when viewing synthetic data

## Communication Protocols

1. **Internet to Raspberry Pi 4**: HTTPS (Port 443)
2. **Raspberry Pi 4 to External Services**: HTTPS
3. **Raspberry Pi 4 to Raspberry Pi 3B**: HTTP over secure local network (Port 8000)
   - Authentication: API Key + IP Restriction
   - Data format: JSON
   - Communication pattern: REST API

## Deployment Considerations

- **Network Segmentation**: Database server (RPi3B) must be on a separate network segment from the web server (RPi4)
- **Firewall Rules**: Only allow specific ports and IP addresses for communication between components
- **VLANs**: Implement VLANs to isolate traffic between different network segments
- **Regular Updates**: Maintain security patches on both devices
- **Data Isolation**: Ensure privacy vault data is protected with additional security measures
- **Demo/Production Separation**: Maintain strict separation between demo and production data

## Integration Points

1. **User Interface ↔ Web Server**: Browser-based communication via HTTPS
2. **Web Server ↔ Database Server**: Internal API communication
3. **Web Server ↔ AI Services**: External API integration
4. **Web Server ↔ Gmail API**: OAuth-based integration
5. **Database Server ↔ Privacy Vault**: Internal encrypted communication
6. **Synthetic Data ↔ Demo Interface**: Controlled access for demonstrations

## Fallback and Recovery

```mermaid
graph TD
    subgraph "Normal Operation"
        A[Web Request] --> B[RPi4 Web Server]
        B --> C[RPi3B Database]
        C --> D[Data Response]
        D --> E[User Response]
    end
    
    subgraph "Fallback Scenarios"
        A --> F{RPi4 Available?}
        F -- No --> G[Show Maintenance Page]
        
        F -- Yes --> H{RPi3B Available?}
        H -- No --> I[Serve Cached Data]
        I --> J[Flag as Potentially Stale]
        J --> E
        
        H -- Yes --> K{Database Intact?}
        K -- No --> L[Restore from Backup]
        L --> C
        
        K -- Yes --> M{Privacy Vault Available?}
        M -- No --> N[Serve Data with Masked Sensitive Fields]
        N --> E
    end
```

## Future Expansion

The architecture is designed to accommodate future enhancements:

1. **Mobile Application**: Additional client interfacing with the same API
2. **Multiple Database Nodes**: Scaling to include additional database servers
3. **Cloud Backup**: Optional secure backup to encrypted cloud storage
4. **Enhanced AI Capabilities**: Integration with more specialized AI models
5. **Additional Data Sources**: Integration with more external systems
6. **Advanced Privacy Controls**: Granular user-defined privacy settings
7. **Extended Demo Capabilities**: Interactive demonstration scenarios 