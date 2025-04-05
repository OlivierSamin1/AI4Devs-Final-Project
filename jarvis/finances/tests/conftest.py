"""
Pytest fixtures for the finances app tests.
"""
import pytest
import json
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import date, timedelta

from finances.models import (
    Bank,
    BankAccount,
    BankCard,
    BankAccountReport,
    FileAccount,
    FileCard,
    FileAccountReport
)
from finances.models.files import File
from .factories import (
    UserFactory,
    BankFactory,
    BankAccountFactory,
    BankCardFactory,
    BankAccountReportFactory,
    FileAccountFactory,
    FileCardFactory,
    FileAccountReportFactory
)


@pytest.fixture
def user():
    """Create a test user."""
    return UserFactory()


@pytest.fixture
def bank():
    """Create a test bank."""
    return BankFactory()


@pytest.fixture
def bank_with_unicode():
    """Create a bank with unicode characters."""
    return BankFactory(
        name="Banque Générale Économique",
        country="Français"
    )


@pytest.fixture
def bank_account(bank, user):
    """Create a test bank account."""
    return BankAccountFactory(bank=bank, titular=user)


@pytest.fixture
def bank_account_closed(bank, user):
    """Create a closed bank account."""
    return BankAccountFactory(
        bank=bank, 
        titular=user,
        is_account_open=False,
        closing_account_date=date.today() - timedelta(days=30)
    )


@pytest.fixture
def bank_account_with_json(bank, user):
    """Create a bank account with complex JSON data."""
    return BankAccountFactory(
        bank=bank,
        titular=user,
        value_on_31_12={
            "2020": 5000.0,
            "2021": 7500.0,
            "2022": 10000.0,
            "2023": 12500.0,
            "notes": {
                "investment": "moderate",
                "growth": "steady"
            }
        }
    )


@pytest.fixture
def bank_card(bank_account):
    """Create a test bank card."""
    return BankCardFactory(bank_account=bank_account)


@pytest.fixture
def inactive_bank_card(bank_account):
    """Create an inactive bank card."""
    return BankCardFactory(
        bank_account=bank_account,
        is_active=False,
        ending_date=date.today() - timedelta(days=30)
    )


@pytest.fixture
def bank_account_report(bank_account):
    """Create a test bank account report."""
    return BankAccountReportFactory(bank_account=bank_account)


@pytest.fixture
def file_account(bank_account):
    """Create a test file for a bank account."""
    return FileAccountFactory(access_to_model=bank_account)


@pytest.fixture
def file_card(bank_card):
    """Create a test file for a bank card."""
    return FileCardFactory(access_to_model=bank_card)


@pytest.fixture
def file_account_report(bank_account_report):
    """Create a test file for a bank account report."""
    return FileAccountReportFactory(access_to_model=bank_account_report)


@pytest.fixture
def test_image():
    """Create a simple test image file."""
    return SimpleUploadedFile(
        name='test_image.jpg',
        content=b'image content',
        content_type='image/jpeg'
    )
