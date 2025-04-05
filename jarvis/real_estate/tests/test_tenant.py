"""
Tests for the Tenant model in the real_estate app.
"""
import pytest
from decimal import Decimal
from django.core.exceptions import ValidationError
from datetime import date

from real_estate.models import Tenant


@pytest.mark.django_db
class TestTenant:
    """Test cases for the Tenant model."""

    def test_create_tenant_with_valid_data(self, tenant):
        """Test creating a tenant with valid data."""
        # Assert that the tenant was created correctly
        assert isinstance(tenant, Tenant)
        assert tenant.id is not None
        assert tenant.asset is not None
        assert tenant.first_name is not None
        assert tenant.last_name is not None

    def test_tenant_str_representation(self, tenant):
        """Test the string representation of a tenant."""
        expected = f"{tenant.first_name} {tenant.last_name}"
        assert str(tenant) == expected

    def test_tenant_without_asset(self, tenant_without_asset):
        """Test a tenant without an asset reference."""
        assert tenant_without_asset.asset is None
        # Should still be a valid tenant
        assert isinstance(tenant_without_asset, Tenant)
        assert tenant_without_asset.id is not None

    def test_tenant_without_name(self, tenant_without_name):
        """Test a tenant without a name."""
        assert tenant_without_name.first_name is None
        assert tenant_without_name.last_name is None
        # String representation should be different
        expected = "Unnamed Tenant"
        assert str(tenant_without_name) == expected

    def test_tenant_with_contact_info(self, tenant_with_contact_info):
        """Test a tenant with contact information."""
        assert tenant_with_contact_info.phone_number == 612345678
        assert tenant_with_contact_info.email == "tenant@example.com"

    def test_tenant_with_id_info(self, tenant_with_id_info):
        """Test a tenant with ID type and number."""
        assert tenant_with_id_info.id_type == "passport"
        assert tenant_with_id_info.id_number == "AB123456"

    def test_tenant_with_bank_info(self, tenant_with_bank_info):
        """Test a tenant with bank account details."""
        assert tenant_with_bank_info.bank_account_IBAN == "ES12 3456 7890 1234 5678 9012"
        assert tenant_with_bank_info.bank_account_recipient == "John Doe"

    def test_tenant_with_dates(self, tenant_with_dates):
        """Test a tenant with rental start/end dates."""
        assert tenant_with_dates.rental_starting_date == date(2022, 1, 1)
        assert tenant_with_dates.rental_ending_date == date(2023, 1, 1)
        
        # Calculate rental duration in months
        rental_duration = ((tenant_with_dates.rental_ending_date.year - 
                            tenant_with_dates.rental_starting_date.year) * 12 +
                            tenant_with_dates.rental_ending_date.month -
                            tenant_with_dates.rental_starting_date.month)
        assert rental_duration == 12

    def test_tenant_with_deposit(self, tenant_with_deposit):
        """Test a tenant with deposit amount."""
        assert tenant_with_deposit.deposit_amount == 1000

    def test_actual_tenant(self, actual_tenant):
        """Test a current tenant."""
        assert actual_tenant.is_actual_tenant is True

    def test_former_tenant(self, former_tenant):
        """Test a former tenant."""
        assert former_tenant.is_actual_tenant is False

    def test_tenant_with_guarantee(self, tenant_with_guarantee):
        """Test a tenant with guarantee."""
        assert tenant_with_guarantee.has_guarantee is True

    def test_tenant_with_comments(self, tenant_with_comments):
        """Test a tenant with comments data."""
        comments = tenant_with_comments.comments
        assert comments is not None
        assert isinstance(comments, dict)
        
        # Check specific comments data
        assert "payment_history" in comments
        assert comments["payment_history"] == "Always on time"
        assert comments["contract_details"] == "1-year contract, renewable"
        
        # Check list in JSON
        assert "special_conditions" in comments
        assert isinstance(comments["special_conditions"], list)
        assert len(comments["special_conditions"]) == 2
        assert "No pets" in comments["special_conditions"] 