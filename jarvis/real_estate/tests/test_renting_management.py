"""
Tests for the Renting Management models in the real_estate app.
"""
import pytest
from decimal import Decimal
from django.core.exceptions import ValidationError
from datetime import date

from real_estate.models import RentingManagementCompany, RentingManagementContract


@pytest.mark.django_db
class TestRentingManagementCompany:
    """Test cases for the RentingManagementCompany model."""

    def test_create_company_with_valid_data(self, renting_company):
        """Test creating a renting management company with valid data."""
        # Assert that the company was created correctly
        assert isinstance(renting_company, RentingManagementCompany)
        assert renting_company.id is not None
        assert renting_company.name is not None

    def test_company_str_representation(self, renting_company):
        """Test the string representation of a renting management company."""
        expected = renting_company.name
        assert str(renting_company) == expected

    def test_company_with_email(self, renting_company_with_email):
        """Test a renting management company with email information."""
        assert renting_company_with_email.personal_email_used == "renting@example.com"

    def test_company_with_comments(self, renting_company_with_comments):
        """Test a renting management company with comments."""
        assert renting_company_with_comments.comments == "High quality property management services"


@pytest.mark.django_db
class TestRentingManagementContract:
    """Test cases for the RentingManagementContract model."""

    def test_create_contract_with_valid_data(self, renting_contract):
        """Test creating a renting management contract with valid data."""
        # Assert that the contract was created correctly
        assert isinstance(renting_contract, RentingManagementContract)
        assert renting_contract.id is not None
        assert renting_contract.company is not None
        assert renting_contract.asset is not None
        assert renting_contract.contract_number is not None

    def test_contract_str_representation(self, renting_contract):
        """Test the string representation of a renting management contract."""
        expected = f"{renting_contract.company.name} - {renting_contract.asset}"
        assert str(renting_contract) == expected

    def test_contract_without_company(self, renting_contract_without_company):
        """Test a contract without a company reference."""
        assert renting_contract_without_company.company is None
        # Should still be a valid contract
        assert isinstance(renting_contract_without_company, RentingManagementContract)
        assert renting_contract_without_company.id is not None
        
        # Check string representation without company
        expected = f"No Company - {renting_contract_without_company.asset}"
        assert str(renting_contract_without_company) == expected

    def test_contract_without_asset(self, renting_contract_without_asset):
        """Test a contract without an asset reference."""
        assert renting_contract_without_asset.asset is None
        # Should still be a valid contract
        assert isinstance(renting_contract_without_asset, RentingManagementContract)
        assert renting_contract_without_asset.id is not None
        
        # Check string representation without asset
        expected = f"{renting_contract_without_asset.company.name} - No Asset"
        assert str(renting_contract_without_asset) == expected

    def test_contract_with_dates(self, renting_contract_with_dates):
        """Test a contract with start and end dates."""
        assert renting_contract_with_dates.starting_date == date(2021, 1, 1)
        assert renting_contract_with_dates.ending_date == date(2023, 1, 1)
        
        # Calculate contract duration in years
        duration_in_years = (renting_contract_with_dates.ending_date.year - 
                             renting_contract_with_dates.starting_date.year)
        assert duration_in_years == 2

    def test_active_contract(self, active_renting_contract):
        """Test an active renting management contract."""
        assert active_renting_contract.is_management_active is True

    def test_inactive_contract(self, inactive_renting_contract):
        """Test an inactive renting management contract."""
        assert inactive_renting_contract.is_management_active is False

    def test_contract_with_results(self, renting_contract_with_results):
        """Test a contract with annual results data."""
        results = renting_contract_with_results.annual_results
        assert results is not None
        assert isinstance(results, dict)
        
        # Check specific year data
        assert "2021" in results
        assert results["2021"]["expenses"] == 1300
        assert results["2021"]["income"] == 9600
        assert results["2021"]["net"] == 8300
        
        # Check all years present
        assert "2022" in results
        
        # Verify specific values for 2022
        assert results["2022"]["expenses"] == 1500
        assert results["2022"]["income"] == 10200
        assert results["2022"]["net"] == 8700
        
        # Verify calculation consistency
        for year in ["2021", "2022"]:
            assert results[year]["net"] == results[year]["income"] - results[year]["expenses"]
            
        # Verify income growth
        assert results["2022"]["income"] > results["2021"]["income"] 