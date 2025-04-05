"""
Tests for the Bill model in the real_estate app.
"""
import pytest
from decimal import Decimal
from django.core.exceptions import ValidationError

from real_estate.models import Bill


@pytest.mark.django_db
class TestBill:
    """Test cases for the Bill model."""

    def test_create_bill_with_valid_data(self, bill):
        """Test creating a bill with valid data."""
        # Assert that the bill was created correctly
        assert isinstance(bill, Bill)
        assert bill.id is not None
        assert bill.asset is not None
        assert bill.client_name is not None
        assert bill.company_name is not None
        assert bill.date is not None
        assert bill.total_price is not None
        assert bill.total_price >= 0

    def test_bill_str_representation(self, bill):
        """Test the string representation of a bill."""
        expected = f"{bill.company_name} - {bill.date}"
        assert str(bill) == expected

    def test_bill_without_asset(self, bill_without_asset):
        """Test a bill without an asset reference."""
        assert bill_without_asset.asset is None
        # Should still be a valid bill
        assert isinstance(bill_without_asset, Bill)
        assert bill_without_asset.id is not None

    def test_bill_without_company(self, bill_without_company):
        """Test a bill without a company name."""
        assert bill_without_company.company_name is None
        # String representation should be different
        expected = f"Unknown Company - {bill_without_company.date}"
        assert str(bill_without_company) == expected

    def test_bill_without_client(self, bill_without_client):
        """Test a bill without a client reference."""
        assert bill_without_client.client_name is None
        # Should still be a valid bill
        assert isinstance(bill_without_client, Bill)
        assert bill_without_client.id is not None

    def test_tax_deductible_bill(self, tax_deductible_bill):
        """Test a tax deductible bill."""
        assert tax_deductible_bill.is_tax_deductible is True

    def test_commission_bill(self, commission_bill):
        """Test a location commission bill."""
        assert commission_bill.is_location_commission_bill is True

    def test_bill_with_prices(self, bill_with_prices):
        """Test a bill with detailed price information."""
        # Check all price fields
        assert bill_with_prices.total_price == Decimal('121.00')
        assert bill_with_prices.tax == Decimal('21.00')
        assert bill_with_prices.price_without_tax == Decimal('100.00')
        
        # Verify price calculation consistency
        assert bill_with_prices.price_without_tax + bill_with_prices.tax == bill_with_prices.total_price 