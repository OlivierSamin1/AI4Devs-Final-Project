"""
Pytest fixtures for the tax app tests.
"""
import pytest
import json
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import date, timedelta

from tax.models import (
    Tax,
    TaxManagementCompany,
    TaxManagementContract,
    FileTax,
    FileTaxManagement
)
from tax.models.files import File
from .factories import (
    UserFactory,
    TaxFactory,
    TaxManagementCompanyFactory,
    TaxManagementContractFactory,
    FileTaxFactory,
    FileTaxManagementFactory
)


@pytest.fixture
def user():
    """Create a test user."""
    return UserFactory()


# Tax Management Company fixtures
@pytest.fixture
def tax_management_company():
    """Create a test tax management company."""
    return TaxManagementCompanyFactory()


@pytest.fixture
def company_with_email():
    """Create a company with email information."""
    return TaxManagementCompanyFactory(
        personal_email_used="contact@taxcompany.com"
    )


@pytest.fixture
def company_with_site():
    """Create a company with site information."""
    return TaxManagementCompanyFactory(
        site_app_company="tax-services.com"
    )


@pytest.fixture
def company_with_comments():
    """Create a company with comments."""
    return TaxManagementCompanyFactory(
        comments="This is a reliable tax management company with extensive experience."
    )


@pytest.fixture
def company_without_name():
    """Create a company without a name."""
    return TaxManagementCompanyFactory(name=None)


# Tax Management Contract fixtures
@pytest.fixture
def tax_management_contract(tax_management_company):
    """Create a test tax management contract."""
    return TaxManagementContractFactory(company=tax_management_company)


@pytest.fixture
def contract_with_number():
    """Create a contract with a specific number."""
    return TaxManagementContractFactory(
        contract_number="TC-123456"
    )


@pytest.fixture
def contract_without_company():
    """Create a contract without a company reference."""
    return TaxManagementContractFactory(company=None)


@pytest.fixture
def contract_with_dates():
    """Create a contract with start and end dates."""
    return TaxManagementContractFactory(
        starting_date=date(2022, 1, 1),
        ending_date=date(2023, 12, 31)
    )


@pytest.fixture
def active_contract():
    """Create an active contract."""
    return TaxManagementContractFactory(
        is_contract_active=True
    )


@pytest.fixture
def inactive_contract():
    """Create an inactive contract."""
    return TaxManagementContractFactory(
        is_contract_active=False
    )


@pytest.fixture
def contract_with_annual_price():
    """Create a contract with annual price data."""
    return TaxManagementContractFactory(
        annual_price={"2022": 400}
    )


@pytest.fixture
def contract_with_multiple_years():
    """Create a contract with price data for multiple years."""
    return TaxManagementContractFactory(
        annual_price={
            "2020": 380,
            "2021": 390,
            "2022": 400,
            "2023": 425
        }
    )


# Tax fixtures
@pytest.fixture
def tax():
    """Create a general test tax."""
    return TaxFactory()


@pytest.fixture
def tax_without_name():
    """Create a tax without a name."""
    return TaxFactory(name=None)


@pytest.fixture
def real_estate_tax(user):
    """Create a real estate tax."""
    return TaxFactory(
        tax_type="Real Estate tax",
        real_estate_tax_type="IVI",
        # real_estate_asset would be set in the test
    )


@pytest.fixture
def transportation_tax(user):
    """Create a transportation tax."""
    return TaxFactory(
        tax_type="Transportation tax",
        # transportation_asset would be set in the test
    )


@pytest.fixture
def person_tax(user):
    """Create a person tax."""
    return TaxFactory(
        tax_type="Person tax",
        person=user
    )


@pytest.fixture
def tax_with_different_types():
    """Create taxes with different types."""
    tax1 = TaxFactory(tax_type="Real Estate tax", real_estate_tax_type="IVI")
    tax2 = TaxFactory(tax_type="Transportation tax")
    tax3 = TaxFactory(tax_type="Person tax")
    tax4 = TaxFactory(tax_type="Other tax")
    return [tax1, tax2, tax3, tax4]


@pytest.fixture
def tax_with_management_company(tax_management_company):
    """Create a tax with a management company."""
    return TaxFactory(
        is_tax_management_company_used=True,
        tax_management_company=tax_management_company
    )


@pytest.fixture
def tax_with_price():
    """Create a tax with a specific yearly price."""
    return TaxFactory(
        yearly_price=1250.75
    )


@pytest.fixture
def tax_with_online_access():
    """Create a tax with online access data."""
    return TaxFactory(
        personal_email_used="personal@taxportal.com",
        site_app="taxportal.gov"
    )


@pytest.fixture
def tax_with_year():
    """Create a tax with a specific year."""
    return TaxFactory(
        year=2023
    )


@pytest.fixture
def real_estate_tax_types():
    """Create taxes with different real estate tax types."""
    tax1 = TaxFactory(tax_type="Real Estate tax", real_estate_tax_type="IVI")
    tax2 = TaxFactory(tax_type="Real Estate tax", real_estate_tax_type="Dustbin")
    tax3 = TaxFactory(tax_type="Real Estate tax", real_estate_tax_type="Other")
    return [tax1, tax2, tax3]


@pytest.fixture
def other_tax_type():
    """Create a tax with custom/other tax type."""
    return TaxFactory(
        tax_type="Other tax"
    )


# File fixtures
@pytest.fixture
def file_tax(tax):
    """Create a test file for a tax."""
    return FileTaxFactory(access_to_model=tax)


@pytest.fixture
def file_tax_management(tax_management_contract):
    """Create a test file for a tax management contract."""
    return FileTaxManagementFactory(access_to_model=tax_management_contract)


@pytest.fixture
def file_without_name():
    """Create a file without a name."""
    return FileTaxFactory(name=None)


@pytest.fixture
def file_with_file_data():
    """Create a file with actual file data."""
    content = SimpleUploadedFile(
        name='test_file.txt',
        content=b'This is a test file content',
        content_type='text/plain'
    )
    return FileTaxFactory(content=content)


@pytest.fixture
def image_file():
    """Create an image file."""
    content = SimpleUploadedFile(
        name='test_image.png',
        content=b'fake image content',
        content_type='image/png'
    )
    return FileTaxFactory(content=content)


@pytest.fixture
def document_file():
    """Create a document file."""
    content = SimpleUploadedFile(
        name='test_document.pdf',
        content=b'fake pdf content',
        content_type='application/pdf'
    )
    return FileTaxFactory(content=content) 