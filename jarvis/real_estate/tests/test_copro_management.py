"""
Tests for the Copro Management models in the real_estate app.
"""
import pytest
from decimal import Decimal
from django.core.exceptions import ValidationError
from datetime import date

from real_estate.models import CoproManagementCompany, CoproManagementContract


@pytest.mark.django_db
class TestCoproManagementCompany:
    """Test cases for the CoproManagementCompany model."""

    def test_create_company_with_valid_data(self, copro_company):
        """Test creating a copro management company with valid data."""
        # Assert that the company was created correctly
        assert isinstance(copro_company, CoproManagementCompany)
        assert copro_company.id is not None
        assert copro_company.name is not None

    def test_company_str_representation(self, copro_company):
        """Test the string representation of a copro management company."""
        expected = copro_company.name
        assert str(copro_company) == expected

    def test_company_with_email(self, copro_company_with_email):
        """Test a copro management company with email information."""
        assert copro_company_with_email.personal_email_used == "copro@example.com"

    def test_company_with_comments(self, copro_company_with_comments):
        """Test a copro management company with comments."""
        assert copro_company_with_comments.comments == "Very responsive company with monthly reports"


@pytest.mark.django_db
class TestCoproManagementContract:
    """Test cases for the CoproManagementContract model."""

    def test_create_contract_with_valid_data(self, copro_contract):
        """Test creating a copro management contract with valid data."""
        # Assert that the contract was created correctly
        assert isinstance(copro_contract, CoproManagementContract)
        assert copro_contract.id is not None
        assert copro_contract.company is not None
        assert copro_contract.asset is not None
        assert copro_contract.contract_number is not None

    def test_contract_str_representation(self, copro_contract):
        """Test the string representation of a copro management contract."""
        expected = f"{copro_contract.company.name} - {copro_contract.asset}"
        assert str(copro_contract) == expected

    def test_contract_without_company(self, copro_contract_without_company):
        """Test a contract without a company reference."""
        assert copro_contract_without_company.company is None
        # Should still be a valid contract
        assert isinstance(copro_contract_without_company, CoproManagementContract)
        assert copro_contract_without_company.id is not None
        
        # Check string representation without company
        expected = f"No Company - {copro_contract_without_company.asset}"
        assert str(copro_contract_without_company) == expected

    def test_contract_without_asset(self, copro_contract_without_asset):
        """Test a contract without an asset reference."""
        assert copro_contract_without_asset.asset is None
        # Should still be a valid contract
        assert isinstance(copro_contract_without_asset, CoproManagementContract)
        assert copro_contract_without_asset.id is not None
        
        # Check string representation without asset
        expected = f"{copro_contract_without_asset.company.name} - No Asset"
        assert str(copro_contract_without_asset) == expected

    def test_contract_with_dates(self, copro_contract_with_dates):
        """Test a contract with start and end dates."""
        assert copro_contract_with_dates.starting_date == date(2021, 1, 1)
        assert copro_contract_with_dates.ending_date == date(2023, 1, 1)
        
        # Calculate contract duration in years
        duration_in_years = (copro_contract_with_dates.ending_date.year - 
                             copro_contract_with_dates.starting_date.year)
        assert duration_in_years == 2

    def test_active_contract(self, active_copro_contract):
        """Test an active copro management contract."""
        assert active_copro_contract.is_management_active is True

    def test_inactive_contract(self, inactive_copro_contract):
        """Test an inactive copro management contract."""
        assert inactive_copro_contract.is_management_active is False

    def test_contract_with_price(self, copro_contract_with_price):
        """Test a contract with pricing data."""
        assert copro_contract_with_price.monthly_price == Decimal('120.00')

    def test_contract_with_expenses(self, copro_contract_with_expenses):
        """Test a contract with annual expenses data."""
        expenses = copro_contract_with_expenses.annual_expenses
        assert expenses is not None
        assert isinstance(expenses, dict)
        
        # Check specific year data
        assert "2021" in expenses
        assert expenses["2021"]["fixed"] == 1200
        assert expenses["2021"]["refurbishment"] == 500
        assert expenses["2021"]["other"] == 300
        assert expenses["2021"]["payment_delay"] == 0
        
        # Check all years present
        assert "2022" in expenses
        
        # Verify specific values for 2022
        assert expenses["2022"]["refurbishment"] == 0
        assert expenses["2022"]["payment_delay"] == 100
        
        # Calculate total expenses for 2021
        total_2021 = (expenses["2021"]["fixed"] + 
                      expenses["2021"]["refurbishment"] + 
                      expenses["2021"]["other"] + 
                      expenses["2021"]["payment_delay"])
        assert total_2021 == 2000 