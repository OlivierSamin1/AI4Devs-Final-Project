"""
Tests for the finances app models.
"""
import pytest
import json
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from datetime import date, timedelta
import uuid

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
    BankFactory,
    BankAccountFactory,
    BankCardFactory,
    BankAccountReportFactory,
    FileAccountFactory,
    FileCardFactory,
    FileAccountReportFactory
)


@pytest.mark.django_db
class TestBank:
    
    def test_create_bank_with_valid_data(self):
        # Arrange & Act
        bank = BankFactory(
            name="Test Bank",
            address="123 Bank Street",
            postal_code=12345,
            country="Test Country"
        )
        
        # Assert
        assert bank.name == "Test Bank"
        assert bank.address == "123 Bank Street"
        assert bank.postal_code == 12345
        assert bank.country == "Test Country"
    
    def test_bank_str_method(self, bank):
        # Arrange
        # bank fixture is already created
        
        # Act
        result = str(bank)
        
        # Assert
        assert result == bank.name
    
    def test_bank_without_name(self):
        # Arrange & Act
        bank = BankFactory(name=None)
        
        # Assert
        assert bank.name is None
    
    def test_bank_meta_ordering(self):
        # Arrange
        bank1 = BankFactory(name="B Bank")
        bank2 = BankFactory(name="A Bank")
        bank3 = BankFactory(name="C Bank")
        
        # Act
        banks = Bank.objects.all()
        
        # Assert
        assert banks[0].name == "A Bank"
        assert banks[1].name == "B Bank"
        assert banks[2].name == "C Bank"
    
    def test_bank_with_unicode_characters(self, bank_with_unicode):
        # Arrange
        # bank_with_unicode fixture is already created
        
        # Act
        result = str(bank_with_unicode)
        
        # Assert
        assert result == "Banque Générale Économique"
        assert bank_with_unicode.country == "Français"
    
    def test_bank_very_long_name(self):
        # Arrange
        long_name = "A" * 50  # Maximum length is 50
        
        # Act
        bank = BankFactory(name=long_name)
        
        # Assert
        assert bank.name == long_name
        assert len(bank.name) == 50
    
    def test_bank_deletion(self, bank):
        # Arrange
        bank_id = bank.id
        
        # Act
        bank.delete()
        
        # Assert
        assert Bank.objects.filter(id=bank_id).count() == 0


@pytest.mark.django_db
class TestBankAccount:
    
    def test_create_account_with_valid_data(self, bank, user):
        # Arrange & Act
        account = BankAccountFactory(
            bank=bank,
            titular=user,
            name="Test Account",
            IBAN="FR7630006000011234567890123",
            BIC="BNPAFRPP123",
            starting_date=date.today(),
            is_account_open=True
        )
        
        # Assert
        assert account.bank == bank
        assert account.titular == user
        assert account.name == "Test Account"
        assert account.IBAN == "FR7630006000011234567890123"
        assert account.BIC == "BNPAFRPP123"
        assert account.starting_date == date.today()
        assert account.is_account_open is True
    
    def test_account_str_method(self, bank_account):
        # Arrange
        # bank_account fixture is already created
        
        # Act
        result = str(bank_account)
        
        # Assert
        assert result == f"{bank_account.bank.name} - {bank_account.name}"
    
    def test_account_balance_calculation(self, bank_account_with_json):
        # Arrange
        account = bank_account_with_json
        
        # Act
        # The value_on_31_12 is a JSONField that contains balance info
        latest_year = max([year for year in account.value_on_31_12.keys() if year.isdigit()])
        balance = account.value_on_31_12[latest_year]
        
        # Assert
        assert balance == 12500.0
    
    def test_account_negative_balance(self, bank, user):
        # Arrange & Act
        account = BankAccountFactory(
            bank=bank,
            titular=user,
            value_on_31_12={"2023": -500.0}
        )
        
        # Assert
        assert account.value_on_31_12["2023"] < 0
    
    def test_account_without_name(self, bank, user):
        # Arrange & Act
        account = BankAccountFactory(
            bank=bank,
            titular=user,
            name=None
        )
        
        # Assert
        assert account.name is None
    
    def test_account_with_institution(self, bank, user):
        # Arrange & Act
        account = BankAccountFactory(
            bank=bank,
            titular=user
        )
        
        # Assert
        assert account.bank == bank
    
    def test_account_number_format(self, bank, user):
        # Arrange
        # Test various IBAN formats
        account1 = BankAccountFactory(bank=bank, titular=user, IBAN="FR7630006000011234567890123")
        account2 = BankAccountFactory(bank=bank, titular=user, IBAN="DE89370400440532013000")
        account3 = BankAccountFactory(bank=bank, titular=user, IBAN="GB29NWBK60161331926819")
        
        # Assert
        assert account1.IBAN.startswith("FR")
        assert account2.IBAN.startswith("DE")
        assert account3.IBAN.startswith("GB")
    
    def test_account_status(self, bank_account, bank_account_closed):
        # Arrange
        # bank_account and bank_account_closed fixtures are already created
        
        # Assert
        assert bank_account.is_account_open is True
        assert bank_account_closed.is_account_open is False
        assert bank_account_closed.closing_account_date is not None
    
    def test_account_long_name(self, bank, user):
        # Arrange
        long_name = "A" * 40  # Maximum length is 40
        
        # Act
        account = BankAccountFactory(
            bank=bank,
            titular=user,
            name=long_name
        )
        
        # Assert
        assert account.name == long_name
        assert len(account.name) == 40
    
    def test_account_unicode_characters(self, bank, user):
        # Arrange & Act
        account = BankAccountFactory(
            bank=bank,
            titular=user,
            name="Compte Épargne"
        )
        
        # Assert
        assert account.name == "Compte Épargne"
    
    def test_account_initial_balance(self, bank, user):
        # Arrange & Act
        account = BankAccountFactory(
            bank=bank,
            titular=user,
            value_on_31_12={"2023": 1000.0}
        )
        
        # Assert
        assert account.value_on_31_12["2023"] == 1000.0
    
    def test_account_owner(self, bank_account, user):
        # Arrange
        # bank_account fixture is already created
        
        # Assert
        assert bank_account.titular == user
    
    def test_account_deletion(self, bank_account):
        # Arrange
        account_id = bank_account.id
        
        # Act
        bank_account.delete()
        
        # Assert
        assert BankAccount.objects.filter(id=account_id).count() == 0
    
    def test_account_with_json_data(self, bank_account_with_json):
        # Arrange
        account = bank_account_with_json
        
        # Assert
        assert account.value_on_31_12["2020"] == 5000.0
        assert account.value_on_31_12["2021"] == 7500.0
        assert account.value_on_31_12["2022"] == 10000.0
        assert account.value_on_31_12["2023"] == 12500.0
        assert account.value_on_31_12["notes"]["investment"] == "moderate"
        assert account.value_on_31_12["notes"]["growth"] == "steady"


@pytest.mark.django_db
class TestBankCard:
    
    def test_create_card_with_valid_data(self, bank_account):
        # Arrange & Act
        card = BankCardFactory(
            bank_account=bank_account,
            name="Test Card",
            is_active=True,
            card_number="4111111111111111",
            ending_date=date.today() + timedelta(days=365),
            CCV="123"
        )
        
        # Assert
        assert card.bank_account == bank_account
        assert card.name == "Test Card"
        assert card.is_active is True
        assert card.card_number == "4111111111111111"
        assert card.ending_date == date.today() + timedelta(days=365)
        assert card.CCV == "123"
    
    def test_card_str_method(self, bank_card):
        # Arrange
        # bank_card fixture is already created
        
        # Act
        result = str(bank_card)
        
        # Assert
        assert result == f"{bank_card.bank_account.bank.name} - {bank_card.name}"
    
    def test_card_without_name(self, bank_account):
        # Arrange & Act
        card = BankCardFactory(
            bank_account=bank_account,
            name=None
        )
        
        # Act
        result = str(card)
        
        # Assert
        assert card.name is None
        assert result == card.bank_account.bank.name
    
    def test_card_status(self, bank_card, inactive_bank_card):
        # Arrange
        # bank_card and inactive_bank_card fixtures are already created
        
        # Assert
        assert bank_card.is_active is True
        assert inactive_bank_card.is_active is False
    
    def test_card_expiry(self, bank_account):
        # Arrange
        expiry_date = date.today() + timedelta(days=730)  # 2 years in the future
        
        # Act
        card = BankCardFactory(
            bank_account=bank_account,
            ending_date=expiry_date
        )
        
        # Assert
        assert card.ending_date == expiry_date
    
    def test_card_number_format(self, bank_account):
        # Arrange & Act
        visa_card = BankCardFactory(
            bank_account=bank_account,
            card_number="4111111111111111"  # Visa pattern
        )
        master_card = BankCardFactory(
            bank_account=bank_account,
            card_number="5555555555554444"  # MasterCard pattern
        )
        amex_card = BankCardFactory(
            bank_account=bank_account,
            card_number="371449635398431"  # Amex pattern
        )
        
        # Assert
        assert visa_card.card_number.startswith("4")
        assert master_card.card_number.startswith("5")
        assert amex_card.card_number.startswith("3")
    
    def test_card_without_bank_account(self):
        # Arrange & Act
        # Check if bank_account field is null=True, which would allow None value
        card = BankCardFactory.build(bank_account=None)
        
        # Assert
        assert card.bank_account is None
        # The field allows null values, so it can be saved in the database
    
    def test_card_deletion(self, bank_card):
        # Arrange
        card_id = bank_card.id
        
        # Act
        bank_card.delete()
        
        # Assert
        assert BankCard.objects.filter(id=card_id).count() == 0


@pytest.mark.django_db
class TestBankAccountReport:
    
    def test_create_report_with_valid_data(self, bank_account):
        # Arrange & Act
        report_date = date.today()
        report = BankAccountReportFactory(
            bank_account=bank_account,
            date=report_date
        )
        
        # Assert
        assert report.bank_account == bank_account
        assert report.date == report_date
    
    def test_report_str_method(self, bank_account_report):
        # Arrange
        # bank_account_report fixture is already created
        report = bank_account_report
        expected_str = f"{report.bank_account} - {report.set_date_to_str()}"
        
        # Act
        result = str(report)
        
        # Assert
        assert result == expected_str
    
    def test_report_set_date_to_str(self, bank_account):
        # Arrange
        test_date = date(2023, 5, 15)
        report = BankAccountReportFactory(
            bank_account=bank_account,
            date=test_date
        )
        expected_date_str = "20235"  # Format: {year}{month}
        
        # Act
        result = report.set_date_to_str()
        
        # Assert
        assert result == expected_date_str
    
    def test_report_without_bank_account(self):
        # Arrange & Act
        # Check if bank_account field is null=True, which would allow None value
        report = BankAccountReportFactory.build(bank_account=None)
        
        # Assert
        assert report.bank_account is None
        # The field allows null values, so it can be created without bank_account
    
    def test_report_without_date(self, bank_account):
        # Arrange & Act
        # Check if date field is null=True, which would allow None value
        report = BankAccountReportFactory.build(
            bank_account=bank_account,
            date=None
        )
        
        # Assert
        assert report.date is None
        # The field allows null values, so it can be created without date
    
    def test_report_ordering(self, bank_account):
        # Arrange
        date1 = date(2023, 1, 1)
        date2 = date(2023, 2, 1)
        date3 = date(2023, 3, 1)
        
        report3 = BankAccountReportFactory(bank_account=bank_account, date=date3)
        report1 = BankAccountReportFactory(bank_account=bank_account, date=date1)
        report2 = BankAccountReportFactory(bank_account=bank_account, date=date2)
        
        # Act
        reports = BankAccountReport.objects.filter(bank_account=bank_account)
        
        # Assert
        assert reports[0] == report1
        assert reports[1] == report2
        assert reports[2] == report3
    
    def test_report_deletion(self, bank_account_report):
        # Arrange
        report_id = bank_account_report.id
        
        # Act
        bank_account_report.delete()
        
        # Assert
        assert BankAccountReport.objects.filter(id=report_id).count() == 0


@pytest.mark.django_db
class TestFile:
    
    def test_file_tag_property(self, file_account):
        # Arrange
        # file_account fixture is already created
        
        # Act
        tag = file_account.file_tag
        
        # Assert
        assert '<img src=' in tag
        assert 'width="500" height="500"' in tag
    
    def test_file_without_name(self, bank_account):
        # Arrange & Act
        file = FileAccountFactory(
            access_to_model=bank_account,
            name=None
        )
        
        # Assert
        assert file.name is None
    
    def test_file_with_content(self, bank_account, test_image):
        # Arrange & Act
        file = FileAccountFactory(
            access_to_model=bank_account,
            content=test_image
        )
        
        # Assert
        assert file.content.name.endswith('.jpg')
        assert file.content.size > 0
    
    def test_file_account_creation(self, bank_account):
        # Arrange & Act
        file = FileAccountFactory(access_to_model=bank_account)
        
        # Assert
        assert file.access_to_model == bank_account
    
    def test_file_card_creation(self, bank_card):
        # Arrange & Act
        file = FileCardFactory(access_to_model=bank_card)
        
        # Assert
        assert file.access_to_model == bank_card
    
    def test_file_account_report_creation(self, bank_account_report):
        # Arrange & Act
        file = FileAccountReportFactory(access_to_model=bank_account_report)
        
        # Assert
        assert file.access_to_model == bank_account_report
    
    def test_file_deletion(self, file_account):
        # Arrange
        file_id = file_account.id
        
        # Act
        file_account.delete()
        
        # Assert
        assert not FileAccount.objects.filter(id=file_id).exists()
