"""
Pytest fixtures for the administrative app tests.
"""
import pytest
import json
from django.core.files.uploadedfile import SimpleUploadedFile

from administrative.models import (
    Document,
    InsuranceCompany,
    InsuranceContract,
    File,
    FileDocument,
    FileInsuranceContract
)
from .factories import (
    DocumentFactory,
    InsuranceCompanyFactory,
    InsuranceContractFactory,
    FileDocumentFactory,
    FileInsuranceContractFactory
)


@pytest.fixture
def document():
    """Create a test document."""
    return DocumentFactory()


@pytest.fixture
def document_with_custom_comment():
    """Create a document with a specific comment."""
    return DocumentFactory(
        comment={"custom_field": "custom_value", "priority": "high"}
    )


@pytest.fixture
def insurance_company():
    """Create a test insurance company."""
    return InsuranceCompanyFactory()


@pytest.fixture
def insurance_contract(insurance_company):
    """Create a test insurance contract."""
    return InsuranceContractFactory(company=insurance_company)


@pytest.fixture
def real_estate_insurance_contract(insurance_company):
    """Create a test insurance contract for real estate."""
    return InsuranceContractFactory(
        company=insurance_company,
        type='Real Estate insurance',
        annual_price={"2023": 400, "2024": 450},
        coverage={"fire": "full", "water_damage": "partial"}
    )


@pytest.fixture
def transportation_insurance_contract(insurance_company):
    """Create a test insurance contract for transportation."""
    return InsuranceContractFactory(
        company=insurance_company,
        type='Transportation insurance',
        annual_price={"2023": 200, "2024": 220},
        coverage={"collision": "full", "theft": "full"}
    )


@pytest.fixture
def person_insurance_contract(insurance_company, user):
    """Create a test insurance contract for a person."""
    return InsuranceContractFactory(
        company=insurance_company,
        type='Person insurance',
        person=user,
        annual_price={"2023": 300, "2024": 330},
        coverage={"health": "full", "disability": "partial"}
    )


@pytest.fixture
def file_document(document):
    """Create a test file attached to a document."""
    return FileDocumentFactory(access_to_model=document)


@pytest.fixture
def file_insurance_contract(insurance_contract):
    """Create a test file attached to an insurance contract."""
    return FileInsuranceContractFactory(access_to_model=insurance_contract)


@pytest.fixture
def test_image():
    """Create a simple test image file."""
    return SimpleUploadedFile(
        name='test_image.jpg',
        content=b'image content',
        content_type='image/jpeg'
    ) 