# Data Dictionary for Administrative Models

## Document Model (`document.py`)

| Field | Type | Description | Constraints |
|-------|------|-------------|------------|
| user | ForeignKey | Reference to Django User model | Can be null, On deletion: CASCADE |
| name | CharField | Name of the document | Max length: 50, Can be null |
| type | CharField | Type of document (ID card, Passport, etc.) | Max length: 50, Can be null, Choices from get_types() function |
| comment | JSONField | Additional comments in JSON format | Can be null and blank |

**Meta Information:**
- Ordering: By type, then name
- Verbose name plural: "Documents"

**Additional Notes:**
- UPLOADED_FILE_PATH is retrieved from environment variables
- Used for storing various identification documents

## File Model (`files.py`)

| Field | Type | Description | Constraints |
|-------|------|-------------|------------|
| name | CharField | Name of the file | Max length: 100, Can be null and blank |
| content | FileField | The actual file content | Uploaded to path from environment variable |

**Meta Information:**
- Verbose name plural: "Files"

**Properties:**
- file_tag: Returns an HTML-safe img tag for displaying file content

## FileDocument Model (`files.py`)

| Field | Type | Description | Constraints |
|-------|------|-------------|------------|
| access_to_model | ForeignKey | Reference to Document model | Can be null and blank, On deletion: CASCADE, Related name: 'document_files' |

**Inheritance:**
- Inherits from File model

## FileInsuranceContract Model (`files.py`)

| Field | Type | Description | Constraints |
|-------|------|-------------|------------|
| access_to_model | ForeignKey | Reference to InsuranceContract model | Can be null and blank, On deletion: CASCADE, Related name: 'insurance_contract_files' |

**Inheritance:**
- Inherits from File model

## InsuranceCompany Model (`insurance_company.py`)

| Field | Type | Description | Constraints |
|-------|------|-------------|------------|
| name | CharField | Name of the insurance company | Max length: 50, Can be null |
| phone_number | PositiveIntegerField | Phone number of the insurance company | Can be null and blank |
| site_app_company | CharField | Website or application URL of the company | Max length: 70, Can be null and blank |

**Meta Information:**
- Ordering: By name, then phone_number
- Verbose name plural: "Insurance Companies"

## InsuranceContract Model (`insurance_contract.py`)

| Field | Type | Description | Constraints |
|-------|------|-------------|------------|
| company | ForeignKey | Reference to InsuranceCompany model | Can be null, On deletion: CASCADE, Related name: 'contract' |
| type | CharField | Type of insurance (Real Estate, Transportation, Person) | Max length: 50, Can be null, Choices from get_types() function |
| real_estate_asset | ForeignKey | Reference to real_estate.Asset model | Can be null and blank, On deletion: CASCADE, Related name: 'insurance_contract' |
| transportation_asset | ForeignKey | Reference to transportation.Asset model | Can be null and blank, On deletion: CASCADE, Related name: 'insurance_contract' |
| person | ForeignKey | Reference to User model | Can be null and blank, On deletion: CASCADE, Related name: 'insurance_contract' |
| contract_number | CharField | Unique identifier for the contract | Max length: 50, Can be null and blank |
| starting_date | DateField | Contract start date | Can be null and blank |
| ending_date | DateField | Contract end date | Can be null and blank |
| is_insurance_active | BooleanField | Status of insurance activity | Can be null and blank |
| personal_email_used | EmailField | Email address used for the contract | Can be null and blank |
| annual_price | JSONField | Yearly prices in JSON format | Can be null and blank |
| coverage | JSONField | Coverage details in JSON format | Can be null and blank |

**Meta Information:**
- Ordering: By company, type, annual_price
- Verbose name plural: "Insurances"

## Admin Configurations (`admin.py`)

### DocumentAdmin
- **Search Fields:** name
- **List Display:** user, type, name
- **List Filter:** user, type
- **Inlines:** FilesInlineDocument

### InsuranceCompanyAdmin
- **Search Fields:** name
- **List Display:** name, phone_number
- **List Filter:** name, phone_number

### InsuranceContractAdmin
- **Search Fields:** company
- **List Display:** company, type, is_insurance_active
- **List Filter:** company, type, is_insurance_active
- **Inlines:** FilesInlineInsuranceContract

### Inline Admins
- **FilesInlineDocument:** Stacked inline for FileDocument objects
- **FilesInlineInsuranceContract:** Stacked inline for FileInsuranceContract objects


# Data Dictionary for Financial Models

## Bank Model
| Field | Type | Description | Constraints |
|-------|------|-------------|------------|
| name | CharField | Name of the bank | max_length=50, null=True, blank=False |
| address | CharField | Physical address of the bank | max_length=200, null=True, blank=True |
| postal_code | PositiveIntegerField | Postal code of the bank | null=True, blank=True |
| country | CharField | Country where the bank is located | max_length=200, null=True, blank=True |

## BankAccount Model
| Field | Type | Description | Constraints |
|-------|------|-------------|------------|
| bank | ForeignKey | Reference to the Bank model | on_delete=CASCADE, null=True, blank=False |
| titular | ForeignKey | Reference to the User model | on_delete=CASCADE, null=True, blank=False |
| name | CharField | Name/label of the account | max_length=40, null=True, blank=False |
| IBAN | CharField | International Bank Account Number | max_length=40, null=True, blank=False |
| BIC | CharField | Bank Identifier Code | max_length=20, null=True, blank=True |
| starting_date | DateField | Date when account was opened | null=True, blank=True |
| ending_date | DateField | Expected end date of the account | null=True, blank=True |
| closing_account_date | DateField | Actual date when account was closed | null=True, blank=True |
| is_account_open | BooleanField | Status of the account (open/closed) | null=True, blank=False, default=True |
| value_on_31_12 | JSONField | Year-end balance for multiple years | null=True, blank=True |

## BankCard Model
| Field | Type | Description | Constraints |
|-------|------|-------------|------------|
| bank_account | ForeignKey | Reference to the BankAccount model | on_delete=CASCADE, null=True, blank=False |
| name | CharField | Name/label of the card | max_length=30, null=True, blank=False |
| is_active | BooleanField | Status of the card (active/inactive) | null=True, blank=False, default=True |
| card_number | CharField | Card number | max_length=16, null=True, blank=True |
| ending_date | DateField | Expiration date of the card | null=True, blank=True |
| CCV | DateField | Security code (Note: This seems to be incorrectly defined as DateField) | null=True, blank=True |

## BankAccountReport Model
| Field | Type | Description | Constraints |
|-------|------|-------------|------------|
| bank_account | ForeignKey | Reference to the BankAccount model | on_delete=CASCADE, null=True, blank=False |
| date | DateField | Date of the report | null=True, blank=False |

## File Model (Base Model)
| Field | Type | Description | Constraints |
|-------|------|-------------|------------|
| name | CharField | Name of the file | max_length=100, null=True, blank=True |
| content | FileField | Actual file stored | upload location set by environment variable |

## FileAccount Model (Extends File)
| Field | Type | Description | Constraints |
|-------|------|-------------|------------|
| access_to_model | ForeignKey | Reference to the BankAccount model | on_delete=CASCADE, null=True, blank=True |

## FileCard Model (Extends File)
| Field | Type | Description | Constraints |
|-------|------|-------------|------------|
| access_to_model | ForeignKey | Reference to the BankCard model | on_delete=CASCADE, null=True, blank=True |

## FileAccountReport Model (Extends File)
| Field | Type | Description | Constraints |
|-------|------|-------------|------------|
| access_to_model | ForeignKey | Reference to the BankAccountReport model | on_delete=CASCADE, null=True, blank=True |

## Admin Registrations
The following models are registered with Django admin:
- BankAccount (with FileAccount inline)
- Bank
- BankCard (with FileCard inline)
- BankAccountReport (with FileAccountReport inline)

## Design Notes
1. The system follows a hierarchical relationship: Bank → BankAccount → BankCard
2. Each entity has associated file storage capabilities
3. The BankAccountReport provides periodic reporting functionality
4. There appears to be commented-out functionality for generating bills from bank account reports


# Health System Data Dictionary

Based on the provided Django models, here's a comprehensive data dictionary detailing each model, its fields, relationships, and purposes within the health insurance system.

## Bill Model

| Field | Type | Constraints | Description |
|-------|------|------------|-------------|
| company_name | CharField(50) | Optional | Name of the health insurance company |
| client_name | ForeignKey(User) | Optional | Reference to the Django User model |
| bill_name | CharField(50) | Required | Descriptive name of the bill |
| date | DateField | Optional | Date when the bill was issued |
| total_price | FloatField | Optional | Total price including tax |
| is_paid | BooleanField | Optional, Default=False | Indicates if the bill has been paid |
| is_asked_by_us | BooleanField | Optional, Default=False | Indicates if the bill was requested by the system users |

**Purpose**: Tracks health-related bills and payments for insurance claims. Associates bills with users and provides payment status tracking.

## File Model (Abstract Base)

| Field | Type | Constraints | Description |
|-------|------|------------|-------------|
| name | CharField(100) | Optional | Name of the file |
| content | FileField | Required | The actual file uploaded to the system |

**Purpose**: Base model for all file types, handles file storage and display functionality.

## FileBill Model

| Field | Type | Constraints | Description |
|-------|------|------------|-------------|
| access_to_model | ForeignKey(Bill) | Optional | Reference to the associated Bill |

**Purpose**: Stores files related to health bills (receipts, claim documents, etc.).

## FileProduct Model

| Field | Type | Constraints | Description |
|-------|------|------------|-------------|
| access_to_model | ForeignKey(Product) | Optional | Reference to the associated Product |

**Purpose**: Stores files related to health products (documentation, images, etc.).

## FileSymptom Model

| Field | Type | Constraints | Description |
|-------|------|------------|-------------|
| access_to_model | ForeignKey(Symptom) | Optional | Reference to the associated Symptom |

**Purpose**: Stores files related to symptoms (reference materials, images, etc.).

## Product Model

| Field | Type | Constraints | Description |
|-------|------|------------|-------------|
| name | CharField(200) | Required | Name of the health product |
| natural | BooleanField | Required | Indicates if the product is natural/organic |
| child_use | BooleanField | Required | Indicates if suitable for children |
| adult_use | BooleanField | Required | Indicates if suitable for adults |
| min_age | CharField(200) | Optional | Minimum age recommendation for use |
| source_info | CharField(200) | Optional | Source of product information |
| date_info | DateField | Optional | Date when information was obtained |
| composition | CharField(200) | Optional | Ingredients or composition details |
| interests | CharField(200) | Optional | Benefits or applications of the product |
| comments | JSONField | Optional | Structured comments about the product |

**Purpose**: Catalogs health products with detailed information about usage recommendations, composition, and benefits.

## Symptom Model

| Field | Type | Constraints | Description |
|-------|------|------------|-------------|
| name | CharField(200) | Required | Name of the symptom |
| child | BooleanField | Required | Indicates if symptom appears in children |
| adult | BooleanField | Required | Indicates if symptom appears in adults |
| products | ManyToManyField(Product) | Optional | Related products that address this symptom |
| comments | JSONField | Optional | Structured comments about the symptom |

**Purpose**: Catalogs health symptoms and associates them with relevant treatment products.

## Admin Configurations

The Django admin interface is configured with custom filters and display options:

- **BillAdmin**: Includes a LastMonthFilter for quick access to recent bills, file uploads, and comprehensive search/filter options
- **ProductAdmin**: Displays product details with file attachment capabilities
- **SymptomAdmin**: Presents symptoms with product relationships and file attachments

**Note**: The system also has an InsuranceContract model in a separate app, which handles various types of insurance (Real Estate, Transportation, Person) with appropriate relationships.

This structure creates a comprehensive health insurance management system that tracks bills, symptoms, and products while maintaining appropriate relationships between entities.


# Real Estate Application Data Dictionary

Below is a comprehensive data dictionary for the models in the real estate application, organized by file.

## asset.py

### Asset
| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| owner | ForeignKey to User | Owner of the real estate asset | Optional |
| nickname | CharField | Custom name for the asset | Required, max 50 chars |
| address | CharField | Physical address | Optional, max 200 chars |
| postal_code | PositiveIntegerField | Postal code | Optional |
| city | CharField | City where asset is located | Optional, max 50 chars |
| country | CharField | Country where asset is located | Optional, max 200 chars |
| bank_accounts | ManyToManyField to BankAccount | Associated bank accounts | Optional |
| buying_date | DateField | Date when asset was purchased | Optional |
| buying_price | PositiveIntegerField | Purchase price | Optional |
| has_on_going_mortgage | BooleanField | Whether asset has an ongoing mortgage | Optional |
| is_rented | BooleanField | Whether asset is currently rented | Optional |
| renting_contract | OneToOneField to RentingManagementContract | Associated renting contract | Optional |
| copro_contract | OneToOneField to CoproManagementContract | Associated co-property contract | Optional |
| is_our_living_house | BooleanField | Whether asset is primary residence | Optional |
| tax_management | ForeignKey to TaxManagementContract | Associated tax management | Optional |
| details | JSONField | Additional details (e.g., notary number) | Optional |
| results_by_year | JSONField | Financial results by year | Optional |

## bills.py

### Bill
| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| asset | ForeignKey to Asset | Associated real estate asset | Required |
| company_name | CharField | Name of the billing company | Optional, max 50 chars |
| client_name | ForeignKey to User | Client associated with bill | Optional |
| bill_name | CharField | Descriptive name for the bill | Required, max 50 chars |
| is_tax_deductible | BooleanField | Whether bill is tax deductible | Optional |
| is_location_commission_bill | BooleanField | Whether bill is for location commission | Optional, default False |
| date | DateField | Date of the bill | Optional |
| total_price | FloatField | Total price including tax | Optional |
| tax | FloatField | Tax amount | Optional |
| price_without_tax | FloatField | Price excluding tax | Optional |

## copro_management.py

### CoproManagementCompany
| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| name | CharField | Name of the co-property management company | Required, max 50 chars |
| personal_email_used | EmailField | Email address used for communication | Optional |
| site_app_company | CharField | Company's website or app | Optional, max 70 chars |
| comments | CharField | Additional comments | Optional, max 500 chars |

### CoproManagementContract
| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| company | OneToOneField to CoproManagementCompany | Associated company | Required |
| contract_number | CharField | Contract reference number | Optional, max 50 chars |
| asset | OneToOneField to Asset | Associated real estate asset | Optional |
| starting_date | DateField | Contract start date | Optional |
| ending_date | DateField | Contract end date | Optional |
| is_management_active | BooleanField | Whether contract is active | Optional |
| monthly_price | FloatField | Monthly management fee | Optional, default 0 |
| year | SmallIntegerField | Contract year | Optional, default 2023 |
| annual_expenses | JSONField | Annual expenses breakdown by year | Optional |

## files.py

### File (Base Model)
| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| name | CharField | Name of the file | Optional, max 100 chars |
| content | FileField | Actual file content | Required |

### Specialized File Models
| Model | Related Model | Relationship |
|-------|--------------|--------------|
| FileAsset | Asset | ForeignKey |
| FileHollyDaysPlatform | HollydaysPlatform | ForeignKey |
| FileHollyDaysReservation | HollydaysReservation | ForeignKey |
| FileBill | Bill | ForeignKey |
| FileCoPro | CoProManagementContract | ForeignKey |
| FileMortgage | Mortgage | ForeignKey |
| FileRenting | RentingManagementContract | ForeignKey |
| FileTenant | Tenant | ForeignKey |
| FileUtility | UtilityContract | ForeignKey |

## hollidays_management.py

### HollydaysPlatform
| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| name | CharField | Name of the holiday platform | Required, max 50 chars |
| personal_email_used | EmailField | Email used for platform | Optional |
| site_app_company | CharField | Platform website or app | Optional, max 70 chars |
| comments | CharField | Additional comments | Optional, max 500 chars |

### HollydaysReservation
| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| platform | ForeignKey to HollydaysPlatform | Associated platform | Required |
| asset | ForeignKey to Asset | Associated real estate asset | Optional |
| reservation_number | CharField | Reservation reference number | Optional, max 50 chars |
| entry_date | DateField | Check-in date | Optional |
| number_of_nights | SmallIntegerField | Duration of stay in nights | Optional |
| end_date | DateField | Check-out date | Optional |
| renting_person_full_name | CharField | Guest's full name | Optional, max 100 chars |
| renting_person_dni | CharField | Guest's ID number | Optional, max 20 chars |
| renting_person_direction | CharField | Guest's address | Optional, max 50 chars |
| renting_person_postcode | CharField | Guest's postal code | Optional, max 50 chars |
| renting_person_city | CharField | Guest's city | Optional, max 50 chars |
| renting_person_region | CharField | Guest's region | Optional, max 50 chars |
| renting_person_country | CharField | Guest's country | Optional, max 50 chars |
| price | FloatField | Reservation price | Optional |
| received_bank | BooleanField | Whether payment received | Optional, default False |
| cleaning | FloatField | Cleaning fee | Optional, default 100 |
| commission_platform | FloatField | Platform commission | Optional, default 0 |
| commission_other | FloatField | Other commissions | Optional, default 0 |
| comments | TextField | Additional comments | Optional |

## mortgage.py

### Mortgage
| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| asset | OneToOneField to Asset | Associated real estate asset | Required |
| name | CharField | Name of the mortgage | Required, max 50 chars |
| bank_account | ForeignKey to BankAccount | Associated bank account | Optional |
| starting_date | DateField | Mortgage start date | Optional |
| ending_date | DateField | Mortgage end date | Optional |
| rate_renegociations | JSONField | Rate renegotiations by year | Optional |
| annual_interests | JSONField | Annual interest payments | Optional |
| annual_capital_refund | JSONField | Annual capital repayments | Optional |
| capital_due_end_of_year | JSONField | Remaining capital at year end | Optional |

## renting_management.py

### RentingManagementCompany
| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| name | CharField | Name of rental management company | Required, max 50 chars |
| personal_email_used | EmailField | Email used for communication | Optional |
| site_app_company | CharField | Company website or app | Optional, max 70 chars |
| comments | CharField | Additional comments | Optional, max 500 chars |

### RentingManagementContract
| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| company | ForeignKey to RentingManagementCompany | Associated company | Required |
| contract_number | CharField | Contract reference number | Optional, max 50 chars |
| asset | OneToOneField to Asset | Associated real estate asset | Optional |
| starting_date | DateField | Contract start date | Optional |
| ending_date | DateField | Contract end date | Optional |
| is_management_active | BooleanField | Whether contract is active | Optional |
| annual_results | JSONField | Annual financial results | Optional |

## tenant.py

### Tenant
| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| asset | OneToOneField to Asset | Associated real estate asset | Required |
| first_name | CharField | Tenant's first name | Required, max 50 chars |
| last_name | CharField | Tenant's last name | Required, max 50 chars |
| phone_number | PositiveIntegerField | Tenant's phone number | Optional |
| email | EmailField | Tenant's email address | Optional |
| id_type | CharField | Type of ID document | Required, max 50 chars |
| id_number | CharField | ID document number | Required, max 50 chars |
| bank_account_IBAN | CharField | Tenant's bank account IBAN | Optional, max 50 chars |
| bank_account_recipient | CharField | Bank account holder name | Optional, max 100 chars |
| rental_starting_date | DateField | Rental contract start date | Required |
| rental_ending_date | DateField | Rental contract end date | Optional |
| deposit_amount | PositiveSmallIntegerField | Security deposit amount | Optional |
| is_actual_tenant | BooleanField | Whether person is current tenant | Required |
| has_guarantee | BooleanField | Whether tenant has guarantor | Optional, default False |
| comments | JSONField | Additional comments | Optional |

## utilities.py

### UtilitySupplier
| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| name | CharField | Name of utility supplier | Required, max 50 chars |
| personal_email_used | EmailField | Email used for communication | Optional |
| phone | CharField | Supplier's phone number | Optional, max 12 chars |
| comments | TextField | Additional comments | Optional |

### UtilityContract
| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| supplier | ForeignKey to UtilitySupplier | Associated supplier | Required |
| user | ForeignKey to User | Associated user | Required |
| personal_email_used | EmailField | Email used for communication | Optional |
| asset | ForeignKey to Asset | Associated real estate asset | Required |
| service | CharField | Type of utility service | Required, choices from UTILITY_CHOICES |
| contract_number | CharField | Contract reference number | Optional, max 50 chars |
| starting_date | DateField | Contract start date | Optional |
| ending_date | DateField | Contract end date | Optional |
| year | SmallIntegerField | Contract year | Optional, default 2023 |
| monthly_price | FloatField | Monthly service fee | Optional, default 0 |
| payment_1 to payment_12 | FloatField | Monthly payments (Jan-Dec) | Optional, default 0 |
| installation_price | FloatField | One-time installation fee | Optional, default 0 |
| date_installation | DateField | Installation date | Optional |
| is_active | BooleanField | Whether contract is active | Optional |
| comments | TextField | Additional comments | Optional |

## insurance_contract.py

### InsuranceContract
| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| company | ForeignKey to InsuranceCompany | Insurance provider | Required |
| type | CharField | Type of insurance | Required, choices from get_types() |
| real_estate_asset | ForeignKey to Asset | Associated real estate asset | Optional, only for Real Estate insurance |
| transportation_asset | ForeignKey to Transportation Asset | Associated transportation asset | Optional, only for Transportation insurance |
| person | ForeignKey to User | Associated person | Optional, only for Person insurance |
| contract_number | CharField | Contract reference number | Optional, max 50 chars |
| starting_date | DateField | Contract start date | Optional |
| ending_date | DateField | Contract end date | Optional |
| is_insurance_active | BooleanField | Whether insurance is active | Optional |
| personal_email_used | EmailField | Email used for communication | Optional |
| annual_price | JSONField | Annual price by year | Optional |
| coverage | JSONField | Insurance coverage details | Optional |



# Data Dictionary for Tax Module Models

## Tax Management Models

### TaxManagementCompany
| Field | Type | Description | Constraints |
|-------|------|-------------|------------|
| name | CharField | Name of the tax management company | max_length=50, non-nullable |
| personal_email_used | EmailField | Email used for communication | nullable |
| site_app_company | CharField | Website or application URL | max_length=70, nullable, example: "myfoncia.com" |
| comments | CharField | Additional notes about the company | max_length=500, nullable |

### TaxManagementContract
| Field | Type | Description | Constraints |
|-------|------|-------------|------------|
| company | ForeignKey | Reference to TaxManagementCompany | nullable, on_delete=CASCADE |
| contract_number | CharField | Unique identifier for the contract | max_length=50, nullable |
| starting_date | DateField | Date when contract begins | nullable |
| ending_date | DateField | Date when contract ends | nullable |
| is_contract_active | BooleanField | Indicates if the contract is active | nullable |
| annual_price | JSONField | Yearly prices by year | nullable, example: {'2020': 400, '2021': 400, ...} |

## Tax Models

### Tax
| Field | Type | Description | Constraints |
|-------|------|-------------|------------|
| name | CharField | Name of the tax | max_length=100, non-nullable |
| tax_type | CharField | Category of tax | max_length=50, choices=["Real Estate tax", "Transportation tax", "Person tax", "Other tax"], nullable |
| real_estate_asset | ForeignKey | Link to real estate property | to 'real_estate.Asset', nullable, only for Real Estate tax |
| real_estate_tax_type | CharField | Specific real estate tax category | max_length=50, choices=["IVI", "Dustbin", "Other"], nullable |
| transportation_asset | ForeignKey | Link to transportation asset | to 'transportation.Asset', nullable, only for Transportation tax |
| year | PositiveSmallIntegerField | Year the tax applies to | nullable |
| person | ForeignKey | Link to User for person-related taxes | to User model, nullable, only for Person tax |
| is_tax_management_company_used | BooleanField | Whether a company manages this tax | nullable, default=False |
| tax_management_company | ForeignKey | Link to management company | to TaxManagementCompany, nullable, only if managed |
| yearly_price | FloatField | Annual cost of the tax | nullable, default=0 |
| personal_email_used | EmailField | Email used for this tax | nullable |
| site_app | CharField | Website for tax management | max_length=70, nullable, example: "impots.gouv.fr" |

## File Models

### File (Base Model)
| Field | Type | Description | Constraints |
|-------|------|-------------|------------|
| name | CharField | Name of the file | max_length=100, nullable |
| content | FileField | Actual file content | uploaded to path from environment variable |
| file_tag | Property | HTML representation of file | Generated HTML image tag |

### FileTax
| Field | Type | Description | Constraints |
|-------|------|-------------|------------|
| *Inherits all fields from File* |  |  |  |
| access_to_model | ForeignKey | Link to associated Tax | to Tax model, nullable, on_delete=CASCADE |

### FileTaxManagement
| Field | Type | Description | Constraints |
|-------|------|-------------|------------|
| *Inherits all fields from File* |  |  |  |
| access_to_model | ForeignKey | Link to associated Tax Management Contract | to TaxManagementContract, nullable, on_delete=CASCADE |

## Admin Configuration

The admin.py file configures the Django admin interface for these models with:

1. **TaxAdmin**:
   - Searchable by name
   - Displays name, tax_type, year, real_estate_tax_type, person, real_estate_asset, transportation_asset
   - Filtered by person, year, tax_type, real_estate_asset, transportation_asset
   - Includes inline FileTax documents

2. **TaxCompanyAdmin**:
   - Searchable by name
   - Displays and filters by name

3. **TaxContractAdmin**:
   - Searchable by company and is_contract_active
   - Displays and filters by company, is_contract_active, annual_price
   - Includes inline FileTaxManagement documents

This data model implements a comprehensive system for tracking various types of taxes, managing tax-related documents, and maintaining relationships with tax management companies.


# Data Dictionary for Transportation Models

## Asset Model

| Field | Type | Description | Constraints |
|-------|------|-------------|------------|
| `owner` | ForeignKey (User) | Reference to the user who owns this transportation asset | Nullable, Optional, related_name='transportation_asset' |
| `type` | CharField | Type of transportation (e.g., Car, bike, moto) | Max length 30, Required |
| `brand` | CharField | Brand/manufacturer of the transportation asset | Max length 30, Required |
| `model` | CharField | Model name of the transportation asset | Max length 50, Optional |
| `registration_number` | CharField | Official registration number | Max length 20, Required, e.g. '6347LMP' |
| `buying_date` | DateField | Date when the asset was purchased | Optional |
| `buying_price` | PositiveInteger | Price paid for the asset | Optional |
| `has_been_bought_new` | BooleanField | Whether the asset was new at purchase | Optional |
| `has_on_going_credit` | BooleanField | Whether there is an active credit for this asset | Optional, Default=False |
| `has_on_going_leasing` | BooleanField | Whether there is an active leasing for this asset | Optional, Default=False |
| `last_itv_date` | DateField | Date of the last technical inspection | Optional |
| `next_itv_date` | DateField | Date of the next scheduled technical inspection | Optional |
| `comments` | JSONField | Additional comments stored as JSON | Optional |

**Meta Information:**
- Ordering: By type, brand, model
- Verbose plural name: "Assets"
- String representation: `type - brand`

## File Model

| Field | Type | Description | Constraints |
|-------|------|-------------|------------|
| `name` | CharField | Name of the file | Max length 100, Optional |
| `content` | FileField | The actual file content | Uploads to path defined in environment variable 'UPLOADING_FILES_FOLDER_PATH' |
| `access_to_model` | ForeignKey (Asset) | Reference to the transportation asset this file is associated with | Nullable, Optional, related_name='transportation_files' |

**Meta Information:**
- Verbose plural name: "Files"
- Additional properties: `file_tag` (returns HTML for displaying file as image)

## Admin Configuration

### AssetAdmin
- Search fields: 'type', 'brand', 'model'
- List display: 'type', 'brand', 'model'
- List filter: Same as list display
- Inlines: FilesInline (allows managing File objects from the Asset admin page)

### FilesInline
- Model: File
- Extra: 0 (no extra empty forms by default)

This structure allows for managing transportation assets with their associated files through the Django admin interface, with appropriate filtering, searching, and inline editing capabilities.


