"""
Tests for the TaxManagementContract model in the tax app.
"""
import pytest
from django.core.exceptions import ValidationError
from datetime import date

from tax.models import TaxManagementContract


@pytest.mark.django_db
class TestTaxManagementContract:
    """Test cases for the TaxManagementContract model."""

    def test_create_contract_with_valid_data(self, tax_management_contract):
        """Test creating a tax management contract with valid data."""
        # Assert that the contract was created correctly
        assert isinstance(tax_management_contract, TaxManagementContract)
        assert tax_management_contract.id is not None
        assert tax_management_contract.company is not None

    def test_contract_str_representation(self, tax_management_contract):
        """Test the string representation of a contract."""
        # Test with company name
        expected = tax_management_contract.company.name
        assert str(tax_management_contract) == expected

    def test_contract_without_company(self, contract_without_company):
        """Test a contract without a company reference."""
        assert contract_without_company.company is None
        # Should still be a valid contract
        assert isinstance(contract_without_company, TaxManagementContract)
        assert contract_without_company.id is not None
        
        # Test str method with None company
        with pytest.raises(AttributeError):
            str(contract_without_company)

    def test_contract_with_number(self, contract_with_number):
        """Test a contract with a contract number."""
        # Assert
        assert contract_with_number.contract_number == "TC-123456"

    def test_contract_with_dates(self, contract_with_dates):
        """Test a contract with start and end dates."""
        # Assert
        assert contract_with_dates.starting_date == date(2022, 1, 1)
        assert contract_with_dates.ending_date == date(2023, 12, 31)
        
        # Check duration
        duration = (contract_with_dates.ending_date - contract_with_dates.starting_date).days
        assert duration == 729  # 2 years (2022-01-01 to 2023-12-31 = 729 days)

    def test_active_contract(self, active_contract):
        """Test an active contract."""
        # Assert
        assert active_contract.is_contract_active is True

    def test_inactive_contract(self, inactive_contract):
        """Test an inactive contract."""
        # Assert
        assert inactive_contract.is_contract_active is False

    def test_contract_with_annual_price(self, contract_with_annual_price):
        """Test a contract with annual price data."""
        # Assert
        assert "2022" in contract_with_annual_price.annual_price
        assert contract_with_annual_price.annual_price["2022"] == 400

    def test_contract_with_multiple_years(self, contract_with_multiple_years):
        """Test a contract with price data for multiple years."""
        # Arrange
        contract = contract_with_multiple_years
        
        # Assert
        assert "2020" in contract.annual_price
        assert "2021" in contract.annual_price
        assert "2022" in contract.annual_price
        assert "2023" in contract.annual_price
        
        # Check values
        assert contract.annual_price["2020"] == 380
        assert contract.annual_price["2021"] == 390
        assert contract.annual_price["2022"] == 400
        assert contract.annual_price["2023"] == 425
        
        # Check increasing trend
        years = sorted([int(year) for year in contract.annual_price.keys() if year.isdigit()])
        prices = [contract.annual_price[str(year)] for year in years]
        
        # Verify prices are increasing
        for i in range(1, len(prices)):
            assert prices[i] > prices[i-1] 