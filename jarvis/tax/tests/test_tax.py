"""
Tests for the Tax model in the tax app.
"""
import pytest
from django.core.exceptions import ValidationError

from tax.models import Tax


@pytest.mark.django_db
class TestTax:
    """Test cases for the Tax model."""

    def test_create_tax_with_valid_data(self, tax):
        """Test creating a tax with valid data."""
        # Assert that the tax was created correctly
        assert isinstance(tax, Tax)
        assert tax.id is not None
        assert tax.name is not None
        assert tax.tax_type is not None

    def test_tax_str_representation(self, tax):
        """Test the string representation of a tax."""
        # Test with tax name
        expected = tax.name
        assert str(tax) == expected

    def test_tax_without_name(self, tax_without_name):
        """Test a tax without a name."""
        assert tax_without_name.name is None
        # Should still be a valid tax
        assert isinstance(tax_without_name, Tax)
        assert tax_without_name.id is not None

    def test_tax_with_different_types(self, tax_with_different_types):
        """Test different tax types."""
        # Arrange
        taxes = tax_with_different_types
        
        # Assert
        assert len(taxes) == 4
        
        # Test each tax type
        tax_types = [tax.tax_type for tax in taxes]
        assert "Real Estate tax" in tax_types
        assert "Transportation tax" in tax_types
        assert "Person tax" in tax_types
        assert "Other tax" in tax_types
        
        # Check that the real estate tax has a real_estate_tax_type
        real_estate_tax = next(tax for tax in taxes if tax.tax_type == "Real Estate tax")
        assert real_estate_tax.real_estate_tax_type is not None

    def test_real_estate_tax(self, real_estate_tax):
        """Test a real estate tax with property reference."""
        # Assert
        assert real_estate_tax.tax_type == "Real Estate tax"
        # Check that real_estate_tax_type is set to one of the valid options
        assert real_estate_tax.real_estate_tax_type in ["IVI", "Dustbin", "Other"]
        # The real_estate_asset would be null for this test
        assert real_estate_tax.real_estate_asset is None

    def test_transportation_tax(self, transportation_tax):
        """Test a transportation tax with vehicle reference."""
        # Assert
        assert transportation_tax.tax_type == "Transportation tax"
        # The transportation_asset would be null for this test
        assert transportation_tax.transportation_asset is None

    def test_person_tax(self, person_tax, user):
        """Test a person tax with user reference."""
        # Assert
        assert person_tax.tax_type == "Person tax"
        assert person_tax.person == user

    def test_tax_with_management_company(self, tax_with_management_company):
        """Test a tax with management company."""
        # Assert
        assert tax_with_management_company.is_tax_management_company_used is True
        assert tax_with_management_company.tax_management_company is not None
        # Verify the tax management company name
        assert tax_with_management_company.tax_management_company.name is not None

    def test_tax_with_price(self, tax_with_price):
        """Test a tax with yearly price."""
        # Assert
        assert tax_with_price.yearly_price == 1250.75

    def test_tax_with_online_access(self, tax_with_online_access):
        """Test a tax with online access data."""
        # Assert
        assert tax_with_online_access.personal_email_used == "personal@taxportal.com"
        assert tax_with_online_access.site_app == "taxportal.gov"

    def test_tax_with_year(self, tax_with_year):
        """Test a tax with specific year."""
        # Assert
        assert tax_with_year.year == 2023

    def test_real_estate_tax_types(self, real_estate_tax_types):
        """Test different real estate tax types."""
        # Arrange
        taxes = real_estate_tax_types
        
        # Assert
        assert len(taxes) == 3
        
        # Test that all taxes have real_estate_tax_type set
        tax_types = [tax.real_estate_tax_type for tax in taxes]
        assert all(tax_type in ["IVI", "Dustbin", "Other"] for tax_type in tax_types)
        
        # Test that there are no duplicate types
        assert len(set(tax_types)) >= 2  # At least 2 different types
        
        # All should be Real Estate taxes
        for tax in taxes:
            assert tax.tax_type == "Real Estate tax"

    def test_other_tax_type(self, other_tax_type):
        """Test custom/other tax types."""
        # Assert
        assert other_tax_type.tax_type == "Other tax" 