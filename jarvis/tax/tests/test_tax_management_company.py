"""
Tests for the TaxManagementCompany model in the tax app.
"""
import pytest
from django.core.exceptions import ValidationError

from tax.models import TaxManagementCompany


@pytest.mark.django_db
class TestTaxManagementCompany:
    """Test cases for the TaxManagementCompany model."""

    def test_create_tax_management_company_with_valid_data(self, tax_management_company):
        """Test creating a tax management company with valid data."""
        # Assert that the company was created correctly
        assert isinstance(tax_management_company, TaxManagementCompany)
        assert tax_management_company.id is not None
        assert tax_management_company.name is not None

    def test_company_str_representation(self, tax_management_company):
        """Test the string representation of a company."""
        # Test with company name
        expected = tax_management_company.name
        assert str(tax_management_company) == expected

    def test_company_without_name(self, company_without_name):
        """Test a company without a name."""
        assert company_without_name.name is None
        # Should still be a valid company
        assert isinstance(company_without_name, TaxManagementCompany)
        assert company_without_name.id is not None

    def test_company_with_email(self, company_with_email):
        """Test a company with email information."""
        # Assert
        assert company_with_email.personal_email_used == "contact@taxcompany.com"

    def test_company_with_site(self, company_with_site):
        """Test a company with site/app URL."""
        # Assert
        assert company_with_site.site_app_company == "tax-services.com"

    def test_company_with_comments(self, company_with_comments):
        """Test a company with comments."""
        # Assert
        assert company_with_comments.comments == "This is a reliable tax management company with extensive experience." 