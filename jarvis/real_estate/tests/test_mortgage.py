"""
Tests for the Mortgage model in the real_estate app.
"""
import pytest
from decimal import Decimal
from django.core.exceptions import ValidationError
from datetime import date

from real_estate.models import Mortgage


@pytest.mark.django_db
class TestMortgage:
    """Test cases for the Mortgage model."""

    def test_create_mortgage_with_valid_data(self, mortgage):
        """Test creating a mortgage with valid data."""
        # Assert that the mortgage was created correctly
        assert isinstance(mortgage, Mortgage)
        assert mortgage.id is not None
        assert mortgage.asset is not None
        assert mortgage.name is not None
        assert mortgage.quantity > 0
        assert mortgage.monthly_payment > 0

    def test_mortgage_str_representation(self, mortgage):
        """Test the string representation of a mortgage."""
        expected = f"{mortgage.name} - {mortgage.asset}"
        assert str(mortgage) == expected

    def test_mortgage_without_asset(self, mortgage_without_asset):
        """Test a mortgage without an asset reference."""
        assert mortgage_without_asset.asset is None
        # Should still be a valid mortgage
        assert isinstance(mortgage_without_asset, Mortgage)
        assert mortgage_without_asset.id is not None
        
        # Check string representation without asset
        expected = f"{mortgage_without_asset.name} - No Asset"
        assert str(mortgage_without_asset) == expected

    def test_mortgage_without_name(self, mortgage_without_name):
        """Test a mortgage without a name."""
        assert mortgage_without_name.name is None
        # String representation should be different
        expected = f"Mortgage for {mortgage_without_name.asset}"
        assert str(mortgage_without_name) == expected

    def test_mortgage_with_dates(self, mortgage_with_dates):
        """Test a mortgage with start and end dates."""
        assert mortgage_with_dates.starting_date == date(2020, 1, 1)
        assert mortgage_with_dates.ending_date == date(2040, 1, 1)
        
        # Calculate loan duration in years
        duration_in_years = (mortgage_with_dates.ending_date.year - 
                             mortgage_with_dates.starting_date.year)
        assert duration_in_years == 20

    def test_mortgage_with_rate_data(self, mortgage_with_rate_data):
        """Test a mortgage with rate renegociation data."""
        rates = mortgage_with_rate_data.rate_renegociations
        assert rates is not None
        assert isinstance(rates, dict)
        
        # Check specific year data
        assert "2020" in rates
        assert rates["2020"] == "2.1%"
        assert rates["2022"] == "1.8%"
        assert rates["2023"] == "1.95%"

    def test_mortgage_with_interest_data(self, mortgage_with_interest_data):
        """Test a mortgage with annual interest data."""
        interests = mortgage_with_interest_data.annual_interests
        assert interests is not None
        assert isinstance(interests, dict)
        
        # Check specific year data
        assert "2020" in interests
        assert interests["2020"] == 4500
        assert interests["2021"] == 4300
        assert interests["2022"] == 4100
        
        # Verify decreasing trend in interests
        assert interests["2020"] > interests["2021"] > interests["2022"]

    def test_mortgage_with_capital_data(self, mortgage_with_capital_data):
        """Test a mortgage with capital refund data."""
        refunds = mortgage_with_capital_data.annual_capital_refund
        assert refunds is not None
        assert isinstance(refunds, dict)
        
        # Check specific year data
        assert "2020" in refunds
        assert refunds["2020"] == 6000
        assert refunds["2021"] == 6200
        assert refunds["2022"] == 6400
        
        # Verify increasing trend in capital refunds
        assert refunds["2020"] < refunds["2021"] < refunds["2022"]

    def test_mortgage_with_capital_due_data(self, mortgage_with_capital_due_data):
        """Test a mortgage with capital due end of year data."""
        capital_due = mortgage_with_capital_due_data.capital_due_end_of_year
        assert capital_due is not None
        assert isinstance(capital_due, dict)
        
        # Check specific year data
        assert "2020" in capital_due
        assert capital_due["2020"] == 194000
        assert capital_due["2021"] == 187800
        assert capital_due["2022"] == 181400
        
        # Verify decreasing trend in capital due
        assert capital_due["2020"] > capital_due["2021"] > capital_due["2022"]
        
        # Check consistency with annual refunds (if both are present)
        if hasattr(mortgage_with_capital_due_data, 'annual_capital_refund'):
            refunds = mortgage_with_capital_due_data.annual_capital_refund
            if "2020" in refunds and "2021" in refunds:
                # Difference between years should equal annual refund
                assert (capital_due["2020"] - capital_due["2021"]) == refunds["2021"] 