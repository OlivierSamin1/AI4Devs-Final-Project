"""
Tests for the Utility models in the real_estate app.
"""
import pytest
from decimal import Decimal
from django.core.exceptions import ValidationError
from datetime import date

from real_estate.models import UtilitySupplier, UtilityContract


@pytest.mark.django_db
class TestUtilitySupplier:
    """Test cases for the UtilitySupplier model."""

    def test_create_supplier_with_valid_data(self, utility_supplier):
        """Test creating a utility supplier with valid data."""
        # Assert that the supplier was created correctly
        assert isinstance(utility_supplier, UtilitySupplier)
        assert utility_supplier.id is not None
        assert utility_supplier.name is not None

    def test_supplier_str_representation(self, utility_supplier):
        """Test the string representation of a utility supplier."""
        expected = utility_supplier.name
        assert str(utility_supplier) == expected

    def test_supplier_with_email(self, utility_supplier_with_email):
        """Test a utility supplier with email information."""
        assert utility_supplier_with_email.personal_email_used == "utility@example.com"

    def test_supplier_with_phone(self, utility_supplier_with_phone):
        """Test a utility supplier with phone information."""
        assert utility_supplier_with_phone.phone == "612345678"

    def test_supplier_with_comments(self, utility_supplier_with_comments):
        """Test a utility supplier with comments."""
        assert utility_supplier_with_comments.comments == "Good customer service, online account management available"


@pytest.mark.django_db
class TestUtilityContract:
    """Test cases for the UtilityContract model."""

    def test_create_contract_with_valid_data(self, utility_contract):
        """Test creating a utility contract with valid data."""
        # Assert that the contract was created correctly
        assert isinstance(utility_contract, UtilityContract)
        assert utility_contract.id is not None
        assert utility_contract.supplier is not None
        assert utility_contract.user is not None
        assert utility_contract.asset is not None
        assert utility_contract.service is not None
        assert utility_contract.contract_number is not None

    def test_contract_str_representation(self, utility_contract):
        """Test the string representation of a utility contract."""
        expected = f"{utility_contract.service} - {utility_contract.supplier.name} - {utility_contract.asset}"
        assert str(utility_contract) == expected

    def test_contract_without_supplier(self, utility_contract_without_supplier):
        """Test a contract without a supplier reference."""
        assert utility_contract_without_supplier.supplier is None
        # Should still be a valid contract
        assert isinstance(utility_contract_without_supplier, UtilityContract)
        assert utility_contract_without_supplier.id is not None
        
        # Check string representation without supplier
        expected = f"{utility_contract_without_supplier.service} - No Supplier - {utility_contract_without_supplier.asset}"
        assert str(utility_contract_without_supplier) == expected

    def test_contract_without_asset(self, utility_contract_without_asset):
        """Test a contract without an asset reference."""
        assert utility_contract_without_asset.asset is None
        # Should still be a valid contract
        assert isinstance(utility_contract_without_asset, UtilityContract)
        assert utility_contract_without_asset.id is not None
        
        # Check string representation without asset
        expected = f"{utility_contract_without_asset.service} - {utility_contract_without_asset.supplier.name} - No Asset"
        assert str(utility_contract_without_asset) == expected

    def test_contract_without_user(self, utility_contract_without_user):
        """Test a contract without a user reference."""
        assert utility_contract_without_user.user is None
        # Should still be a valid contract
        assert isinstance(utility_contract_without_user, UtilityContract)
        assert utility_contract_without_user.id is not None

    def test_electricity_contract(self, electricity_contract):
        """Test an electricity contract."""
        assert electricity_contract.service == "Electricity"

    def test_water_contract(self, water_contract):
        """Test a water contract."""
        assert water_contract.service == "Water"

    def test_internet_contract(self, internet_contract):
        """Test an internet contract."""
        assert internet_contract.service == "Internet"

    def test_contract_with_dates(self, utility_contract_with_dates):
        """Test a contract with start and end dates."""
        assert utility_contract_with_dates.starting_date == date(2022, 1, 1)
        assert utility_contract_with_dates.ending_date == date(2023, 1, 1)
        
        # Calculate contract duration in months
        duration_in_months = ((utility_contract_with_dates.ending_date.year - 
                             utility_contract_with_dates.starting_date.year) * 12 +
                             utility_contract_with_dates.ending_date.month -
                             utility_contract_with_dates.starting_date.month)
        assert duration_in_months == 12

    def test_active_contract(self, active_utility_contract):
        """Test an active utility contract."""
        assert active_utility_contract.is_active is True

    def test_inactive_contract(self, inactive_utility_contract):
        """Test an inactive utility contract."""
        assert inactive_utility_contract.is_active is False

    def test_contract_with_price(self, utility_contract_with_price):
        """Test a contract with monthly price."""
        assert utility_contract_with_price.monthly_price == Decimal('75.50')

    def test_contract_with_payments(self, utility_contract_with_payments):
        """Test a contract with payment data."""
        # Check monthly price
        assert utility_contract_with_payments.monthly_price == Decimal('80.00')
        
        # Check individual payments
        assert utility_contract_with_payments.payment_1 == Decimal('80.00')
        assert utility_contract_with_payments.payment_2 == Decimal('85.00')
        assert utility_contract_with_payments.payment_3 == Decimal('75.00')
        assert utility_contract_with_payments.payment_12 == Decimal('75.00')
        
        # Calculate average payment
        total_payments = (
            utility_contract_with_payments.payment_1 +
            utility_contract_with_payments.payment_2 +
            utility_contract_with_payments.payment_3 +
            utility_contract_with_payments.payment_4 +
            utility_contract_with_payments.payment_5 +
            utility_contract_with_payments.payment_6 +
            utility_contract_with_payments.payment_7 +
            utility_contract_with_payments.payment_8 +
            utility_contract_with_payments.payment_9 +
            utility_contract_with_payments.payment_10 +
            utility_contract_with_payments.payment_11 +
            utility_contract_with_payments.payment_12
        )
        avg_payment = total_payments / 12
        # Compare with a tolerance for floating point
        assert abs(avg_payment - Decimal('79.58')) < Decimal('0.01')

    def test_contract_with_installation(self, utility_contract_with_installation):
        """Test a contract with installation details."""
        assert utility_contract_with_installation.installation_price == Decimal('250.00')
        assert utility_contract_with_installation.date_installation == date(2022, 1, 15)

    def test_contract_with_comments(self, utility_contract_with_comments):
        """Test a contract with comments."""
        assert utility_contract_with_comments.comments == "Upgraded to fiber optic in January 2022. 24 month contract." 