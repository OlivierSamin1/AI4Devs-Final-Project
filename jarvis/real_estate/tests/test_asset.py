"""
Tests for the Asset model in the real_estate app.
"""
import pytest
from decimal import Decimal
from django.core.exceptions import ValidationError

from real_estate.models import Asset


@pytest.mark.django_db
class TestAsset:
    """Test cases for the Asset model."""

    def test_create_asset_with_valid_data(self, asset):
        """Test creating an asset with valid data."""
        # Assert that the asset was created correctly
        assert isinstance(asset, Asset)
        assert asset.id is not None
        assert asset.owner is not None
        assert asset.address is not None
        assert asset.postal_code is not None
        assert asset.city is not None
        assert asset.country is not None

    def test_asset_str_representation(self, asset):
        """Test the string representation of an asset."""
        # Test with address first
        expected = f"{asset.address}, {asset.postal_code} {asset.city}, {asset.country}"
        assert str(asset) == expected

        # Test with nickname if available
        asset.nickname = "Beach House"
        expected = "Beach House"
        assert str(asset) == expected

    def test_asset_without_owner(self, asset_without_owner):
        """Test an asset without an owner reference."""
        assert asset_without_owner.owner is None
        # Should still be a valid asset
        assert isinstance(asset_without_owner, Asset)
        assert asset_without_owner.id is not None

    def test_asset_without_nickname(self, asset_without_nickname):
        """Test an asset without a nickname."""
        assert asset_without_nickname.nickname is None
        # String representation should fall back to address
        expected = f"{asset_without_nickname.address}, {asset_without_nickname.postal_code} {asset_without_nickname.city}, {asset_without_nickname.country}"
        assert str(asset_without_nickname) == expected

    def test_asset_with_mortgage_flag(self, asset_with_mortgage_flag):
        """Test an asset with the mortgage flag set."""
        assert asset_with_mortgage_flag.has_on_going_mortgage is True

    def test_asset_with_renting_status(self, asset_with_renting_status):
        """Test an asset with the renting status set."""
        assert asset_with_renting_status.is_rented is True

    def test_asset_as_living_house(self, asset_as_living_house):
        """Test an asset marked as primary residence."""
        assert asset_as_living_house.is_our_living_house is True

    def test_asset_with_buying_details(self, asset_with_buying_details):
        """Test an asset with buying date and price."""
        assert asset_with_buying_details.buying_date is not None
        assert asset_with_buying_details.buying_price is not None
        assert asset_with_buying_details.buying_price > 0

    def test_asset_with_address(self, asset_with_address):
        """Test an asset with full address information."""
        assert asset_with_address.address == "123 Test Street"
        assert asset_with_address.postal_code == 12345
        assert asset_with_address.city == "Test City"
        assert asset_with_address.country == "Test Country"

    def test_asset_with_json_details(self, asset_with_json_details):
        """Test an asset with complex JSON details."""
        details = asset_with_json_details.details
        assert details is not None
        assert isinstance(details, dict)
        assert details["notary_number"] == 12345
        assert details["floors"] == 2
        assert details["bedrooms"] == 3
        assert details["bathrooms"] == 2
        
        # Test nested list in JSON
        assert "renovation_history" in details
        assert isinstance(details["renovation_history"], list)
        assert len(details["renovation_history"]) == 2
        assert details["renovation_history"][0]["year"] == 2015
        assert details["renovation_history"][1]["cost"] == 8000

    def test_asset_with_results(self, asset_with_results):
        """Test an asset with yearly results data."""
        results = asset_with_results.results_by_year
        assert results is not None
        assert isinstance(results, dict)
        
        # Check specific year data
        assert "2020" in results
        assert results["2020"]["income"] == 12000
        assert results["2020"]["expenses"] == 5000
        assert results["2020"]["profit"] == 7000
        
        # Check all years present
        assert "2021" in results
        assert "2022" in results 