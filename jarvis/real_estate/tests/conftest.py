"""
Pytest fixtures for the real_estate app tests.
"""
import pytest
import json
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import date, timedelta

from real_estate.models import (
    Asset,
    Bill,
    Mortgage,
    Tenant,
    CoproManagementCompany,
    CoproManagementContract,
    RentingManagementCompany,
    RentingManagementContract,
    UtilitySupplier,
    UtilityContract,
    HollydaysPlatform,
    HollydaysReservation,
    File,
    FileAsset,
    FileBill,
    FileMortgage,
    FileTenant,
    FileCoPro,
    FileRenting,
    FileUtility,
    FileHollyDaysPlatform,
    FileHollyDaysReservation
)
from .factories import (
    UserFactory,
    AssetFactory,
    BillFactory,
    MortgageFactory,
    TenantFactory,
    CoproManagementCompanyFactory,
    CoproManagementContractFactory,
    RentingManagementCompanyFactory,
    RentingManagementContractFactory,
    UtilitySupplierFactory,
    UtilityContractFactory,
    HollydaysPlatformFactory,
    HollydaysReservationFactory,
    FileAssetFactory,
    FileBillFactory,
    FileMortgageFactory,
    FileTenantFactory,
    FileCoProFactory,
    FileRentingFactory,
    FileUtilityFactory,
    FileHollyDaysPlatformFactory,
    FileHollyDaysReservationFactory
)


# User fixtures
@pytest.fixture
def user():
    """Create a test user."""
    return UserFactory()


# Asset fixtures
@pytest.fixture
def asset(user):
    """Create a test asset."""
    return AssetFactory(owner=user)


@pytest.fixture
def asset_without_owner():
    """Create an asset without owner reference."""
    return AssetFactory(owner=None)


@pytest.fixture
def asset_without_nickname():
    """Create an asset without nickname."""
    return AssetFactory(nickname=None)


@pytest.fixture
def asset_with_address():
    """Create an asset with address information."""
    return AssetFactory(
        address="123 Test Street",
        postal_code=12345,
        city="Test City",
        country="Test Country"
    )


@pytest.fixture
def asset_with_buying_details():
    """Create an asset with buying date and price."""
    return AssetFactory(
        buying_date=date(2020, 1, 15),
        buying_price=250000
    )


@pytest.fixture
def asset_with_mortgage_flag():
    """Create an asset with mortgage flag."""
    return AssetFactory(has_on_going_mortgage=True)


@pytest.fixture
def asset_with_renting_status():
    """Create an asset with renting status."""
    return AssetFactory(is_rented=True)


@pytest.fixture
def asset_as_living_house():
    """Create an asset as primary residence."""
    return AssetFactory(is_our_living_house=True)


@pytest.fixture
def asset_with_json_details():
    """Create an asset with complex JSON details."""
    return AssetFactory(
        details={
            "notary_number": 12345,
            "floors": 2,
            "bedrooms": 3,
            "bathrooms": 2,
            "parking_spaces": 1,
            "construction_year": 2010,
            "renovation_history": [
                {"year": 2015, "type": "kitchen", "cost": 15000},
                {"year": 2018, "type": "bathroom", "cost": 8000}
            ]
        }
    )


@pytest.fixture
def asset_with_results():
    """Create an asset with yearly results data."""
    return AssetFactory(
        results_by_year={
            "2020": {"income": 12000, "expenses": 5000, "profit": 7000},
            "2021": {"income": 12500, "expenses": 4800, "profit": 7700},
            "2022": {"income": 13000, "expenses": 5200, "profit": 7800}
        }
    )


# Bill fixtures
@pytest.fixture
def bill(asset, user):
    """Create a test bill."""
    return BillFactory(asset=asset, client_name=user)


@pytest.fixture
def bill_without_asset():
    """Create a bill without asset reference."""
    return BillFactory(asset=None)


@pytest.fixture
def bill_without_company():
    """Create a bill without company name."""
    return BillFactory(company_name=None)


@pytest.fixture
def bill_without_client():
    """Create a bill without client reference."""
    return BillFactory(client_name=None)


@pytest.fixture
def tax_deductible_bill(asset):
    """Create a tax deductible bill."""
    return BillFactory(asset=asset, is_tax_deductible=True)


@pytest.fixture
def commission_bill(asset):
    """Create a location commission bill."""
    return BillFactory(asset=asset, is_location_commission_bill=True)


@pytest.fixture
def bill_with_prices(asset):
    """Create a bill with detailed price information."""
    return BillFactory(
        asset=asset,
        total_price=121.00,
        tax=21.00,
        price_without_tax=100.00
    )


# Mortgage fixtures
@pytest.fixture
def mortgage(asset_with_mortgage_flag):
    """Create a test mortgage."""
    return MortgageFactory(asset=asset_with_mortgage_flag)


@pytest.fixture
def mortgage_without_asset():
    """Create a mortgage without asset reference."""
    return MortgageFactory(asset=None)


@pytest.fixture
def mortgage_without_name():
    """Create a mortgage without name."""
    return MortgageFactory(name=None)


@pytest.fixture
def mortgage_with_dates(asset_with_mortgage_flag):
    """Create a mortgage with start and end dates."""
    return MortgageFactory(
        asset=asset_with_mortgage_flag,
        starting_date=date(2020, 1, 1),
        ending_date=date(2040, 1, 1)
    )


@pytest.fixture
def mortgage_with_rate_data(asset_with_mortgage_flag):
    """Create a mortgage with rate renegociation data."""
    return MortgageFactory(
        asset=asset_with_mortgage_flag,
        rate_renegociations={
            "2020": "2.1%",
            "2022": "1.8%",
            "2023": "1.95%"
        }
    )


@pytest.fixture
def mortgage_with_interest_data(asset_with_mortgage_flag):
    """Create a mortgage with annual interest data."""
    return MortgageFactory(
        asset=asset_with_mortgage_flag,
        annual_interests={
            "2020": 4500,
            "2021": 4300,
            "2022": 4100
        }
    )


@pytest.fixture
def mortgage_with_capital_data(asset_with_mortgage_flag):
    """Create a mortgage with capital refund data."""
    return MortgageFactory(
        asset=asset_with_mortgage_flag,
        annual_capital_refund={
            "2020": 6000,
            "2021": 6200,
            "2022": 6400
        }
    )


@pytest.fixture
def mortgage_with_capital_due_data(asset_with_mortgage_flag):
    """Create a mortgage with capital due end of year data."""
    return MortgageFactory(
        asset=asset_with_mortgage_flag,
        capital_due_end_of_year={
            "2020": 194000,
            "2021": 187800,
            "2022": 181400
        }
    )


# Tenant fixtures
@pytest.fixture
def tenant(asset_with_renting_status):
    """Create a test tenant."""
    return TenantFactory(asset=asset_with_renting_status)


@pytest.fixture
def tenant_without_asset():
    """Create a tenant without asset reference."""
    return TenantFactory(asset=None)


@pytest.fixture
def tenant_without_name():
    """Create a tenant without name."""
    return TenantFactory(first_name=None, last_name=None)


@pytest.fixture
def tenant_with_contact_info(asset_with_renting_status):
    """Create a tenant with contact information."""
    return TenantFactory(
        asset=asset_with_renting_status,
        phone_number=612345678,
        email="tenant@example.com"
    )


@pytest.fixture
def tenant_with_id_info(asset_with_renting_status):
    """Create a tenant with ID type and number."""
    return TenantFactory(
        asset=asset_with_renting_status,
        id_type="passport",
        id_number="AB123456"
    )


@pytest.fixture
def tenant_with_bank_info(asset_with_renting_status):
    """Create a tenant with bank account details."""
    return TenantFactory(
        asset=asset_with_renting_status,
        bank_account_IBAN="ES12 3456 7890 1234 5678 9012",
        bank_account_recipient="John Doe"
    )


@pytest.fixture
def tenant_with_dates(asset_with_renting_status):
    """Create a tenant with rental start/end dates."""
    return TenantFactory(
        asset=asset_with_renting_status,
        rental_starting_date=date(2022, 1, 1),
        rental_ending_date=date(2023, 1, 1)
    )


@pytest.fixture
def tenant_with_deposit(asset_with_renting_status):
    """Create a tenant with deposit amount."""
    return TenantFactory(
        asset=asset_with_renting_status,
        deposit_amount=1000
    )


@pytest.fixture
def actual_tenant(asset_with_renting_status):
    """Create a current tenant."""
    return TenantFactory(
        asset=asset_with_renting_status,
        is_actual_tenant=True
    )


@pytest.fixture
def former_tenant(asset_with_renting_status):
    """Create a former tenant."""
    return TenantFactory(
        asset=asset_with_renting_status,
        is_actual_tenant=False
    )


@pytest.fixture
def tenant_with_guarantee(asset_with_renting_status):
    """Create a tenant with guarantee."""
    return TenantFactory(
        asset=asset_with_renting_status,
        has_guarantee=True
    )


@pytest.fixture
def tenant_with_comments(asset_with_renting_status):
    """Create a tenant with comments data."""
    return TenantFactory(
        asset=asset_with_renting_status,
        comments={
            "payment_history": "Always on time",
            "contract_details": "1-year contract, renewable",
            "special_conditions": ["No pets", "Non-smoking"],
            "personal_notes": "Very clean and respectful tenant"
        }
    )


# Copro Management fixtures
@pytest.fixture
def copro_company():
    """Create a test copro management company."""
    return CoproManagementCompanyFactory()


@pytest.fixture
def copro_company_with_email():
    """Create a copro company with email information."""
    return CoproManagementCompanyFactory(
        personal_email_used="copro@example.com"
    )


@pytest.fixture
def copro_company_with_comments():
    """Create a copro company with comments."""
    return CoproManagementCompanyFactory(
        comments="Very responsive company with monthly reports"
    )


@pytest.fixture
def copro_contract(copro_company, asset):
    """Create a test copro management contract."""
    return CoproManagementContractFactory(
        company=copro_company,
        asset=asset
    )


@pytest.fixture
def copro_contract_without_company(asset):
    """Create a contract without company."""
    return CoproManagementContractFactory(
        company=None,
        asset=asset
    )


@pytest.fixture
def copro_contract_without_asset(copro_company):
    """Create a contract without asset."""
    return CoproManagementContractFactory(
        company=copro_company,
        asset=None
    )


@pytest.fixture
def copro_contract_with_dates(copro_company, asset):
    """Create a contract with start/end dates."""
    return CoproManagementContractFactory(
        company=copro_company,
        asset=asset,
        starting_date=date(2021, 1, 1),
        ending_date=date(2023, 1, 1)
    )


@pytest.fixture
def active_copro_contract(copro_company, asset):
    """Create an active contract."""
    return CoproManagementContractFactory(
        company=copro_company,
        asset=asset,
        is_management_active=True
    )


@pytest.fixture
def inactive_copro_contract(copro_company, asset):
    """Create an inactive contract."""
    return CoproManagementContractFactory(
        company=copro_company,
        asset=asset,
        is_management_active=False
    )


@pytest.fixture
def copro_contract_with_price(copro_company, asset):
    """Create a contract with pricing data."""
    return CoproManagementContractFactory(
        company=copro_company,
        asset=asset,
        monthly_price=120.00
    )


@pytest.fixture
def copro_contract_with_expenses(copro_company, asset):
    """Create a contract with annual expenses data."""
    return CoproManagementContractFactory(
        company=copro_company,
        asset=asset,
        annual_expenses={
            "2021": {
                "fixed": 1200,
                "refurbishment": 500,
                "other": 300,
                "payment_delay": 0
            },
            "2022": {
                "fixed": 1250,
                "refurbishment": 0,
                "other": 200,
                "payment_delay": 100
            }
        }
    )


# Renting Management fixtures
@pytest.fixture
def renting_company():
    """Create a test renting management company."""
    return RentingManagementCompanyFactory()


@pytest.fixture
def renting_company_with_email():
    """Create a renting company with email information."""
    return RentingManagementCompanyFactory(
        personal_email_used="renting@example.com"
    )


@pytest.fixture
def renting_company_with_comments():
    """Create a renting company with comments."""
    return RentingManagementCompanyFactory(
        comments="High quality property management services"
    )


@pytest.fixture
def renting_contract(renting_company, asset_with_renting_status):
    """Create a test renting management contract."""
    return RentingManagementContractFactory(
        company=renting_company,
        asset=asset_with_renting_status
    )


@pytest.fixture
def renting_contract_without_company(asset_with_renting_status):
    """Create a contract without company."""
    return RentingManagementContractFactory(
        company=None,
        asset=asset_with_renting_status
    )


@pytest.fixture
def renting_contract_without_asset(renting_company):
    """Create a contract without asset."""
    return RentingManagementContractFactory(
        company=renting_company,
        asset=None
    )


@pytest.fixture
def renting_contract_with_dates(renting_company, asset_with_renting_status):
    """Create a contract with start/end dates."""
    return RentingManagementContractFactory(
        company=renting_company,
        asset=asset_with_renting_status,
        starting_date=date(2021, 1, 1),
        ending_date=date(2023, 1, 1)
    )


@pytest.fixture
def active_renting_contract(renting_company, asset_with_renting_status):
    """Create an active contract."""
    return RentingManagementContractFactory(
        company=renting_company,
        asset=asset_with_renting_status,
        is_management_active=True
    )


@pytest.fixture
def inactive_renting_contract(renting_company, asset_with_renting_status):
    """Create an inactive contract."""
    return RentingManagementContractFactory(
        company=renting_company,
        asset=asset_with_renting_status,
        is_management_active=False
    )


@pytest.fixture
def renting_contract_with_results(renting_company, asset_with_renting_status):
    """Create a contract with annual results data."""
    return RentingManagementContractFactory(
        company=renting_company,
        asset=asset_with_renting_status,
        annual_results={
            "2021": {
                "expenses": 1300,
                "income": 9600,
                "net": 8300
            },
            "2022": {
                "expenses": 1500,
                "income": 10200,
                "net": 8700
            }
        }
    )


# Utility fixtures
@pytest.fixture
def utility_supplier():
    """Create a test utility supplier."""
    return UtilitySupplierFactory()


@pytest.fixture
def utility_supplier_with_email():
    """Create a supplier with email information."""
    return UtilitySupplierFactory(
        personal_email_used="utility@example.com"
    )


@pytest.fixture
def utility_supplier_with_phone():
    """Create a supplier with phone information."""
    return UtilitySupplierFactory(
        phone="612345678"
    )


@pytest.fixture
def utility_supplier_with_comments():
    """Create a supplier with comments."""
    return UtilitySupplierFactory(
        comments="Good customer service, online account management available"
    )


@pytest.fixture
def utility_contract(utility_supplier, user, asset):
    """Create a test utility contract."""
    return UtilityContractFactory(
        supplier=utility_supplier,
        user=user,
        asset=asset
    )


@pytest.fixture
def utility_contract_without_supplier(user, asset):
    """Create a contract without supplier."""
    return UtilityContractFactory(
        supplier=None,
        user=user,
        asset=asset
    )


@pytest.fixture
def utility_contract_without_asset(utility_supplier, user):
    """Create a contract without asset."""
    return UtilityContractFactory(
        supplier=utility_supplier,
        user=user,
        asset=None
    )


@pytest.fixture
def utility_contract_without_user(utility_supplier, asset):
    """Create a contract without user."""
    return UtilityContractFactory(
        supplier=utility_supplier,
        user=None,
        asset=asset
    )


@pytest.fixture
def electricity_contract(utility_supplier, user, asset):
    """Create an electricity contract."""
    return UtilityContractFactory(
        supplier=utility_supplier,
        user=user,
        asset=asset,
        service="Electricity"
    )


@pytest.fixture
def water_contract(utility_supplier, user, asset):
    """Create a water contract."""
    return UtilityContractFactory(
        supplier=utility_supplier,
        user=user,
        asset=asset,
        service="Water"
    )


@pytest.fixture
def internet_contract(utility_supplier, user, asset):
    """Create an internet contract."""
    return UtilityContractFactory(
        supplier=utility_supplier,
        user=user,
        asset=asset,
        service="Internet"
    )


@pytest.fixture
def utility_contract_with_dates(utility_supplier, user, asset):
    """Create a contract with start/end dates."""
    return UtilityContractFactory(
        supplier=utility_supplier,
        user=user,
        asset=asset,
        starting_date=date(2022, 1, 1),
        ending_date=date(2023, 1, 1)
    )


@pytest.fixture
def active_utility_contract(utility_supplier, user, asset):
    """Create an active contract."""
    return UtilityContractFactory(
        supplier=utility_supplier,
        user=user,
        asset=asset,
        is_active=True
    )


@pytest.fixture
def inactive_utility_contract(utility_supplier, user, asset):
    """Create an inactive contract."""
    return UtilityContractFactory(
        supplier=utility_supplier,
        user=user,
        asset=asset,
        is_active=False
    )


@pytest.fixture
def utility_contract_with_price(utility_supplier, user, asset):
    """Create a contract with monthly price."""
    return UtilityContractFactory(
        supplier=utility_supplier,
        user=user,
        asset=asset,
        monthly_price=75.50
    )


@pytest.fixture
def utility_contract_with_payments(utility_supplier, user, asset):
    """Create a contract with payment data."""
    return UtilityContractFactory(
        supplier=utility_supplier,
        user=user,
        asset=asset,
        monthly_price=80.00,
        payment_1=80.00,
        payment_2=85.00,
        payment_3=75.00,
        payment_4=70.00,
        payment_5=65.00,
        payment_6=85.00,
        payment_7=90.00,
        payment_8=95.00,
        payment_9=80.00,
        payment_10=75.00,
        payment_11=70.00,
        payment_12=75.00
    )


@pytest.fixture
def utility_contract_with_installation(utility_supplier, user, asset):
    """Create a contract with installation details."""
    return UtilityContractFactory(
        supplier=utility_supplier,
        user=user,
        asset=asset,
        installation_price=250.00,
        date_installation=date(2022, 1, 15)
    )


@pytest.fixture
def utility_contract_with_comments(utility_supplier, user, asset):
    """Create a contract with comments."""
    return UtilityContractFactory(
        supplier=utility_supplier,
        user=user,
        asset=asset,
        comments="Upgraded to fiber optic in January 2022. 24 month contract."
    )


# Holidays Management fixtures
@pytest.fixture
def holidays_platform():
    """Create a test holidays platform."""
    return HollydaysPlatformFactory()


@pytest.fixture
def holidays_platform_with_email():
    """Create a platform with email information."""
    return HollydaysPlatformFactory(
        personal_email_used="holidays@example.com"
    )


@pytest.fixture
def holidays_platform_with_site():
    """Create a platform with site/app information."""
    return HollydaysPlatformFactory(
        site_app_company="bookings.example.com"
    )


@pytest.fixture
def holidays_platform_with_comments():
    """Create a platform with comments."""
    return HollydaysPlatformFactory(
        comments="Platform charges 15% commission, biweekly payouts, good support channel"
    )


@pytest.fixture
def holidays_reservation(holidays_platform, asset):
    """Create a test holidays reservation."""
    return HollydaysReservationFactory(
        platform=holidays_platform,
        asset=asset
    )


@pytest.fixture
def holidays_reservation_without_platform(asset):
    """Create a reservation without platform."""
    return HollydaysReservationFactory(
        platform=None,
        asset=asset
    )


@pytest.fixture
def holidays_reservation_without_asset(holidays_platform):
    """Create a reservation without asset."""
    return HollydaysReservationFactory(
        platform=holidays_platform,
        asset=None
    )


@pytest.fixture
def holidays_reservation_with_number(holidays_platform, asset):
    """Create a reservation with reservation number."""
    return HollydaysReservationFactory(
        platform=holidays_platform,
        asset=asset,
        reservation_number="BOOK-12345"
    )


@pytest.fixture
def holidays_reservation_with_dates(holidays_platform, asset):
    """Create a reservation with entry/end dates."""
    entry_date = date(2022, 7, 15)
    end_date = date(2022, 7, 22)
    return HollydaysReservationFactory(
        platform=holidays_platform,
        asset=asset,
        entry_date=entry_date,
        end_date=end_date,
        number_of_nights=(end_date - entry_date).days
    )


@pytest.fixture
def holidays_reservation_with_nights(holidays_platform, asset):
    """Create a reservation with number of nights."""
    entry_date = date(2022, 8, 10)
    nights = 5
    return HollydaysReservationFactory(
        platform=holidays_platform,
        asset=asset,
        entry_date=entry_date,
        number_of_nights=nights,
        end_date=entry_date + timedelta(days=nights)
    )


@pytest.fixture
def holidays_reservation_with_renter(holidays_platform, asset):
    """Create a reservation with renting person details."""
    return HollydaysReservationFactory(
        platform=holidays_platform,
        asset=asset,
        renting_person_full_name="Jane Smith",
        renting_person_dni="ID12345",
        renting_person_direction="123 Tourist St",
        renting_person_postcode="54321",
        renting_person_city="Tourist City",
        renting_person_region="Tourist Region",
        renting_person_country="Tourist Country"
    )


@pytest.fixture
def holidays_reservation_with_price(holidays_platform, asset):
    """Create a reservation with price information."""
    return HollydaysReservationFactory(
        platform=holidays_platform,
        asset=asset,
        price=850.00
    )


@pytest.fixture
def holidays_reservation_received(holidays_platform, asset):
    """Create a reservation with received bank status."""
    return HollydaysReservationFactory(
        platform=holidays_platform,
        asset=asset,
        received_bank=True
    )


@pytest.fixture
def holidays_reservation_with_cleaning(holidays_platform, asset):
    """Create a reservation with cleaning information."""
    return HollydaysReservationFactory(
        platform=holidays_platform,
        asset=asset,
        cleaning=120.00
    )


@pytest.fixture
def holidays_reservation_with_commission(holidays_platform, asset):
    """Create a reservation with commission information."""
    return HollydaysReservationFactory(
        platform=holidays_platform,
        asset=asset,
        commission_platform=85.00,
        commission_other=25.00
    )


@pytest.fixture
def holidays_reservation_with_comments(holidays_platform, asset):
    """Create a reservation with comments."""
    return HollydaysReservationFactory(
        platform=holidays_platform,
        asset=asset,
        comments="Family of 4, repeated guests, no special requests"
    )


# File fixtures
@pytest.fixture
def test_image():
    """Create a simple test image file."""
    return SimpleUploadedFile(
        name='test_image.jpg',
        content=b'image content',
        content_type='image/jpeg'
    )


@pytest.fixture
def test_document():
    """Create a simple test document file."""
    return SimpleUploadedFile(
        name='test_document.pdf',
        content=b'document content',
        content_type='application/pdf'
    )


@pytest.fixture
def file_asset(asset):
    """Create a test file for an asset."""
    return FileAssetFactory(access_to_model=asset)


@pytest.fixture
def file_bill(bill):
    """Create a test file for a bill."""
    return FileBillFactory(access_to_model=bill)


@pytest.fixture
def file_mortgage(mortgage):
    """Create a test file for a mortgage."""
    return FileMortgageFactory(access_to_model=mortgage)


@pytest.fixture
def file_tenant(tenant):
    """Create a test file for a tenant."""
    return FileTenantFactory(access_to_model=tenant)


@pytest.fixture
def file_copro(copro_contract):
    """Create a test file for a copro contract."""
    return FileCoProFactory(access_to_model=copro_contract)


@pytest.fixture
def file_renting(renting_contract):
    """Create a test file for a renting contract."""
    return FileRentingFactory(access_to_model=renting_contract)


@pytest.fixture
def file_utility(utility_contract):
    """Create a test file for a utility contract."""
    return FileUtilityFactory(access_to_model=utility_contract)


@pytest.fixture
def file_holidays_platform(holidays_platform):
    """Create a test file for a holidays platform."""
    return FileHollyDaysPlatformFactory(access_to_model=holidays_platform)


@pytest.fixture
def file_holidays_reservation(holidays_reservation):
    """Create a test file for a holidays reservation."""
    return FileHollyDaysReservationFactory(access_to_model=holidays_reservation) 