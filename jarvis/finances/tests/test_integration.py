"""
Integration tests for the finances app models.
These tests verify the interactions between different models.
"""
import pytest
from datetime import date, timedelta
from django.contrib.auth import get_user_model

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

User = get_user_model()


@pytest.mark.django_db
class TestFinancesIntegration:
    
    def test_account_with_multiple_transactions(self, bank_account_with_json):
        """Test an account with multiple yearly balance entries."""
        # Arrange
        account = bank_account_with_json
        
        # Assert
        balances = [value for key, value in account.value_on_31_12.items() if key.isdigit()]
        assert len(balances) == 4  # 2020, 2021, 2022, 2023
        # Check for increasing balance trend
        assert balances[0] < balances[1] < balances[2] < balances[3]
    
    def test_bank_with_multiple_accounts(self, bank, user):
        """Test bank with multiple associated accounts."""
        # Arrange
        account1 = BankAccountFactory(bank=bank, titular=user, name="Checking")
        account2 = BankAccountFactory(bank=bank, titular=user, name="Savings")
        account3 = BankAccountFactory(bank=bank, titular=user, name="Investment")
        
        # Act
        bank_accounts = BankAccount.objects.filter(bank=bank)
        
        # Assert
        assert bank_accounts.count() == 3
        assert set(bank_accounts.values_list('name', flat=True)) == {"Checking", "Savings", "Investment"}
    
    def test_account_with_multiple_cards(self, bank_account):
        """Test account with multiple associated cards."""
        # Arrange
        card1 = BankCardFactory(bank_account=bank_account, name="Visa")
        card2 = BankCardFactory(bank_account=bank_account, name="Mastercard")
        card3 = BankCardFactory(bank_account=bank_account, name="Amex")
        
        # Act
        cards = BankCard.objects.filter(bank_account=bank_account)
        
        # Assert
        assert cards.count() == 3
        assert set(cards.values_list('name', flat=True)) == {"Visa", "Mastercard", "Amex"}
    
    def test_account_with_multiple_reports(self, bank_account):
        """Test account with multiple monthly reports."""
        # Arrange
        date1 = date(2023, 1, 1)
        date2 = date(2023, 2, 1)
        date3 = date(2023, 3, 1)
        
        report1 = BankAccountReportFactory(bank_account=bank_account, date=date1)
        report2 = BankAccountReportFactory(bank_account=bank_account, date=date2)
        report3 = BankAccountReportFactory(bank_account=bank_account, date=date3)
        
        # Act
        reports = BankAccountReport.objects.filter(bank_account=bank_account)
        
        # Assert
        assert reports.count() == 3
        assert list(reports.order_by('date').values_list('date', flat=True)) == [date1, date2, date3]
    
    def test_account_with_multiple_files(self, bank_account):
        """Test account with multiple attached files."""
        # Arrange
        file1 = FileAccountFactory(access_to_model=bank_account, name="Statement 1")
        file2 = FileAccountFactory(access_to_model=bank_account, name="Statement 2")
        file3 = FileAccountFactory(access_to_model=bank_account, name="Contract")
        
        # Act
        files = FileAccount.objects.filter(access_to_model=bank_account)
        
        # Assert
        assert files.count() == 3
        assert set(files.values_list('name', flat=True)) == {"Statement 1", "Statement 2", "Contract"}
    
    def test_card_with_multiple_files(self, bank_card):
        """Test card with multiple attached files."""
        # Arrange
        file1 = FileCardFactory(access_to_model=bank_card, name="Card Front")
        file2 = FileCardFactory(access_to_model=bank_card, name="Card Back")
        file3 = FileCardFactory(access_to_model=bank_card, name="Pin Letter")
        
        # Act
        files = FileCard.objects.filter(access_to_model=bank_card)
        
        # Assert
        assert files.count() == 3
        assert set(files.values_list('name', flat=True)) == {"Card Front", "Card Back", "Pin Letter"}
    
    def test_report_with_file(self, bank_account_report):
        """Test report with attached file."""
        # Arrange
        file = FileAccountReportFactory(access_to_model=bank_account_report, name="Monthly Report")
        
        # Act
        files = FileAccountReport.objects.filter(access_to_model=bank_account_report)
        
        # Assert
        assert files.count() == 1
        assert files.first().name == "Monthly Report"
    
    def test_bank_cascade_delete(self, bank, user):
        """Test that deleting a bank cascades to accounts."""
        # Arrange
        account1 = BankAccountFactory(bank=bank, titular=user)
        account2 = BankAccountFactory(bank=bank, titular=user)
        
        account_ids = [account1.id, account2.id]
        
        # Act
        bank.delete()
        
        # Assert
        assert BankAccount.objects.filter(id__in=account_ids).count() == 0
    
    def test_account_cascade_delete(self, bank_account):
        """Test that deleting an account cascades to cards, reports, and files."""
        # Arrange
        card = BankCardFactory(bank_account=bank_account)
        report = BankAccountReportFactory(bank_account=bank_account)
        file_account = FileAccountFactory(access_to_model=bank_account)
        
        card_id = card.id
        report_id = report.id
        file_id = file_account.id
        
        # Act
        bank_account.delete()
        
        # Assert
        assert not BankCard.objects.filter(id=card_id).exists()
        assert not BankAccountReport.objects.filter(id=report_id).exists()
        assert not FileAccount.objects.filter(id=file_id).exists()
    
    def test_user_financial_overview(self, user):
        """Test retrieving all financial data for a user."""
        # Arrange
        bank1 = BankFactory(name="Bank A")
        bank2 = BankFactory(name="Bank B")
        
        account1 = BankAccountFactory(bank=bank1, titular=user, name="Checking A")
        account2 = BankAccountFactory(bank=bank1, titular=user, name="Savings A")
        account3 = BankAccountFactory(bank=bank2, titular=user, name="Checking B")
        
        card1 = BankCardFactory(bank_account=account1)
        card2 = BankCardFactory(bank_account=account3)
        
        # Act
        user_accounts = BankAccount.objects.filter(titular=user)
        account_ids = user_accounts.values_list('id', flat=True)
        user_cards = BankCard.objects.filter(bank_account__in=account_ids)
        
        # Assert
        assert user_accounts.count() == 3
        assert user_cards.count() == 2
        assert set(user_accounts.values_list('bank__name', flat=True)) == {"Bank A", "Bank B"}
    
    def test_account_balance_history(self, bank, user):
        """Test account balance history over time."""
        # Arrange
        account = BankAccountFactory(
            bank=bank,
            titular=user,
            value_on_31_12={
                "2020": 5000.0,
                "2021": 7500.0,
                "2022": 10000.0,
                "2023": 12500.0
            }
        )
        
        # Act - Calculate growth between years
        growth_2020_2021 = account.value_on_31_12["2021"] - account.value_on_31_12["2020"]
        growth_2021_2022 = account.value_on_31_12["2022"] - account.value_on_31_12["2021"]
        growth_2022_2023 = account.value_on_31_12["2023"] - account.value_on_31_12["2022"]
        
        # Assert
        assert growth_2020_2021 == 2500.0
        assert growth_2021_2022 == 2500.0
        assert growth_2022_2023 == 2500.0
    
    def test_multi_bank_account_relationship(self, user):
        """Test user having accounts at multiple banks."""
        # Arrange
        bank1 = BankFactory(name="First Bank")
        bank2 = BankFactory(name="Second Bank")
        bank3 = BankFactory(name="Third Bank")
        
        account1 = BankAccountFactory(bank=bank1, titular=user)
        account2 = BankAccountFactory(bank=bank2, titular=user)
        account3 = BankAccountFactory(bank=bank3, titular=user)
        
        # Act
        user_banks = Bank.objects.filter(account__titular=user).distinct()
        
        # Assert
        assert user_banks.count() == 3
        assert set(user_banks.values_list('name', flat=True)) == {"First Bank", "Second Bank", "Third Bank"}
    
    def test_account_lifecycle(self, bank, user):
        """Test full account lifecycle - creation, cards, reports, closure."""
        # Arrange - Create account
        account = BankAccountFactory(
            bank=bank,
            titular=user,
            starting_date=date(2020, 1, 1),
            is_account_open=True
        )
        
        # Add cards
        card = BankCardFactory(bank_account=account)
        
        # Add reports
        report = BankAccountReportFactory(bank_account=account)
        
        # Add file
        file = FileAccountFactory(access_to_model=account)
        
        # Act - Close the account
        account.is_account_open = False
        account.closing_account_date = date.today()
        account.save()
        
        # Deactivate card
        card.is_active = False
        card.save()
        
        # Assert
        updated_account = BankAccount.objects.get(id=account.id)
        updated_card = BankCard.objects.get(id=card.id)
        
        assert updated_account.is_account_open is False
        assert updated_account.closing_account_date == date.today()
        assert updated_card.is_active is False
    
    def test_full_financial_structure(self, user):
        """Test the complete financial structure of a user."""
        # Arrange
        # Create bank
        bank = BankFactory()
        
        # Create accounts
        checking = BankAccountFactory(bank=bank, titular=user, name="Checking")
        savings = BankAccountFactory(bank=bank, titular=user, name="Savings")
        
        # Create cards
        debit_card = BankCardFactory(bank_account=checking, name="Debit Card")
        credit_card = BankCardFactory(bank_account=checking, name="Credit Card")
        
        # Create reports
        checking_report = BankAccountReportFactory(bank_account=checking)
        savings_report = BankAccountReportFactory(bank_account=savings)
        
        # Create files
        checking_file = FileAccountFactory(access_to_model=checking)
        savings_file = FileAccountFactory(access_to_model=savings)
        debit_card_file = FileCardFactory(access_to_model=debit_card)
        credit_card_file = FileCardFactory(access_to_model=credit_card)
        
        # Act
        user_accounts = BankAccount.objects.filter(titular=user)
        user_cards = BankCard.objects.filter(bank_account__in=user_accounts)
        user_reports = BankAccountReport.objects.filter(bank_account__in=user_accounts)
        account_files = FileAccount.objects.filter(access_to_model__in=user_accounts)
        card_files = FileCard.objects.filter(access_to_model__in=user_cards)
        
        # Assert
        assert user_accounts.count() == 2
        assert user_cards.count() == 2
        assert user_reports.count() == 2
        assert account_files.count() == 2
        assert card_files.count() == 2
    
    def test_file_relationships(self, bank_account, bank_card, bank_account_report):
        """Test file relationships across different models."""
        # Arrange
        file_account = FileAccountFactory(access_to_model=bank_account)
        file_card = FileCardFactory(access_to_model=bank_card)
        file_report = FileAccountReportFactory(access_to_model=bank_account_report)
        
        # Act - Get files through relationships
        account_files = bank_account.BankAccount_files.all()
        card_files = bank_card.BankCard_files.all()
        report_files = bank_account_report.FileAccountReport.all()
        
        # Assert
        assert account_files.count() == 1
        assert account_files.first() == file_account
        
        assert card_files.count() == 1
        assert card_files.first() == file_card
        
        assert report_files.count() == 1
        assert report_files.first() == file_report
    
    def test_cross_model_file_reference(self, bank_account, bank_card):
        """Test file objects reference correct model types."""
        # Arrange
        file_account = FileAccountFactory(access_to_model=bank_account)
        file_card = FileCardFactory(access_to_model=bank_card)
        
        # Act & Assert
        assert file_account.access_to_model._meta.model_name == 'bankaccount'
        assert file_card.access_to_model._meta.model_name == 'bankcard'
    
    def test_user_with_multiple_bank_relationships(self, user):
        """Test user with multiple banks and accounts."""
        # Arrange
        number_of_banks = 3
        accounts_per_bank = 2
        
        banks = [BankFactory() for _ in range(number_of_banks)]
        
        # Create multiple accounts per bank
        for bank in banks:
            for i in range(accounts_per_bank):
                BankAccountFactory(bank=bank, titular=user, name=f"Account {i+1}")
        
        # Act
        user_accounts = BankAccount.objects.filter(titular=user)
        
        # Assert
        assert user_accounts.count() == number_of_banks * accounts_per_bank
        # Check that we have the right number of accounts per bank
        for bank in banks:
            bank_accounts = user_accounts.filter(bank=bank)
            assert bank_accounts.count() == accounts_per_bank
