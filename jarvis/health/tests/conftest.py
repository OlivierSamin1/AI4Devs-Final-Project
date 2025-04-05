"""
Pytest fixtures for the health app tests.
"""
import pytest
import json
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import date, timedelta

from health.models import (
    Bill, 
    Product,
    Symptom,
    FileBill,
    FileProduct,
    FileSymptom
)
from health.models.files import File
from .factories import (
    UserFactory,
    BillFactory,
    ProductFactory,
    SymptomFactory,
    FileBillFactory, 
    FileProductFactory,
    FileSymptomFactory
)


@pytest.fixture
def user():
    """Create a test user."""
    return UserFactory()


@pytest.fixture
def bill(user):
    """Create a test bill."""
    return BillFactory(client_name=user)


@pytest.fixture
def bill_without_company():
    """Create a bill without company name."""
    return BillFactory(company_name=None)


@pytest.fixture
def bill_without_client():
    """Create a bill without client reference."""
    return BillFactory(client_name=None)


@pytest.fixture
def paid_bill(user):
    """Create a paid bill."""
    return BillFactory(
        client_name=user,
        is_paid=True
    )


@pytest.fixture
def unpaid_bill(user):
    """Create an unpaid bill."""
    return BillFactory(
        client_name=user, 
        is_paid=False
    )


@pytest.fixture
def asked_by_us_bill(user):
    """Create a bill that was asked by us."""
    return BillFactory(
        client_name=user,
        is_asked_by_us=True
    )


@pytest.fixture
def product():
    """Create a test product."""
    return ProductFactory()


@pytest.fixture
def natural_product():
    """Create a natural product."""
    return ProductFactory(natural=True)


@pytest.fixture
def child_product():
    """Create a product for children."""
    return ProductFactory(
        child_use=True,
        adult_use=False,
        min_age="2"
    )


@pytest.fixture
def adult_product():
    """Create a product for adults."""
    return ProductFactory(
        child_use=False,
        adult_use=True,
        min_age="18"
    )


@pytest.fixture
def product_with_comments():
    """Create a product with detailed comments."""
    return ProductFactory(
        comments={
            "usage": "Take 2 tablets daily",
            "side_effects": "Nausea, headache, dizziness",
            "storage": "Keep below 25°C",
            "ingredients": ["active_ingredient_1", "active_ingredient_2"],
            "research": {
                "studies": 3,
                "findings": "Effective in 85% of cases",
                "publication_dates": ["2020-01-15", "2021-03-20", "2022-05-10"]
            }
        }
    )


@pytest.fixture
def symptom():
    """Create a test symptom."""
    return SymptomFactory()


@pytest.fixture
def child_symptom():
    """Create a symptom for children."""
    return SymptomFactory(
        child=True, 
        adult=False
    )


@pytest.fixture
def adult_symptom():
    """Create a symptom for adults."""
    return SymptomFactory(
        child=False,
        adult=True
    )


@pytest.fixture
def symptom_with_products(symptom, product, natural_product):
    """Create a symptom with associated products."""
    symptom.products.add(product)
    symptom.products.add(natural_product)
    return symptom


@pytest.fixture
def symptom_with_comments():
    """Create a symptom with detailed comments."""
    return SymptomFactory(
        comments={
            "severity": ["mild", "moderate", "severe"],
            "duration": "1-2 weeks",
            "common_causes": ["viral infection", "bacterial infection", "allergy"],
            "preventive_measures": "Hand washing, avoiding contact with sick people",
            "risk_factors": {
                "age": "Children under 5 and adults over 65",
                "conditions": ["immunodeficiency", "chronic respiratory disease"]
            }
        }
    )


@pytest.fixture
def file_bill(bill):
    """Create a test file for a bill."""
    return FileBillFactory(access_to_model=bill)


@pytest.fixture
def file_product(product):
    """Create a test file for a product."""
    return FileProductFactory(access_to_model=product)


@pytest.fixture
def file_symptom(symptom):
    """Create a test file for a symptom."""
    return FileSymptomFactory(access_to_model=symptom)


@pytest.fixture
def test_image():
    """Create a simple test image file."""
    return SimpleUploadedFile(
        name='test_image.jpg',
        content=b'image content',
        content_type='image/jpeg'
    ) 