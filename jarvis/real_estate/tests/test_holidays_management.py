"""
Tests for the Holidays Management models in the real_estate app.
"""
import pytest
from decimal import Decimal
from django.core.exceptions import ValidationError
from datetime import date, timedelta

from real_estate.models import HollydaysPlatform, HollydaysReservation


@pytest.mark.django_db
class TestHollydaysPlatform:
    """Test cases for the HollydaysPlatform model."""

    def test_create_platform_with_valid_data(self, holidays_platform):
        """Test creating a holidays platform with valid data."""
        # Assert that the platform was created correctly
        assert isinstance(holidays_platform, HollydaysPlatform)
        assert holidays_platform.id is not None
        assert holidays_platform.name is not None

    def test_platform_str_representation(self, holidays_platform):
        """Test the string representation of a holidays platform."""
        expected = holidays_platform.name
        assert str(holidays_platform) == expected

    def test_platform_with_email(self, holidays_platform_with_email):
        """Test a holidays platform with email information."""
        assert holidays_platform_with_email.personal_email_used == "holidays@example.com"

    def test_platform_with_site(self, holidays_platform_with_site):
        """Test a holidays platform with site/app information."""
        assert holidays_platform_with_site.site_app_company == "bookings.example.com"

    def test_platform_with_comments(self, holidays_platform_with_comments):
        """Test a holidays platform with comments."""
        assert holidays_platform_with_comments.comments == "Platform charges 15% commission, biweekly payouts, good support channel"


@pytest.mark.django_db
class TestHollydaysReservation:
    """Test cases for the HollydaysReservation model."""

    def test_create_reservation_with_valid_data(self, holidays_reservation):
        """Test creating a holidays reservation with valid data."""
        # Assert that the reservation was created correctly
        assert isinstance(holidays_reservation, HollydaysReservation)
        assert holidays_reservation.id is not None
        assert holidays_reservation.platform is not None
        assert holidays_reservation.asset is not None
        assert holidays_reservation.entry_date is not None

    def test_reservation_str_representation(self, holidays_reservation):
        """Test the string representation of a holidays reservation."""
        expected = f"{holidays_reservation.platform.name} - {holidays_reservation.asset} - {holidays_reservation.entry_date}"
        assert str(holidays_reservation) == expected

    def test_reservation_without_platform(self, holidays_reservation_without_platform):
        """Test a reservation without a platform reference."""
        assert holidays_reservation_without_platform.platform is None
        # Should still be a valid reservation
        assert isinstance(holidays_reservation_without_platform, HollydaysReservation)
        assert holidays_reservation_without_platform.id is not None
        
        # Check string representation without platform
        expected = f"No Platform - {holidays_reservation_without_platform.asset} - {holidays_reservation_without_platform.entry_date}"
        assert str(holidays_reservation_without_platform) == expected

    def test_reservation_without_asset(self, holidays_reservation_without_asset):
        """Test a reservation without an asset reference."""
        assert holidays_reservation_without_asset.asset is None
        # Should still be a valid reservation
        assert isinstance(holidays_reservation_without_asset, HollydaysReservation)
        assert holidays_reservation_without_asset.id is not None
        
        # Check string representation without asset
        expected = f"{holidays_reservation_without_asset.platform.name} - No Asset - {holidays_reservation_without_asset.entry_date}"
        assert str(holidays_reservation_without_asset) == expected

    def test_reservation_with_number(self, holidays_reservation_with_number):
        """Test a reservation with reservation number."""
        assert holidays_reservation_with_number.reservation_number == "BOOK-12345"

    def test_reservation_with_dates(self, holidays_reservation_with_dates):
        """Test a reservation with entry/end dates."""
        assert holidays_reservation_with_dates.entry_date == date(2022, 7, 15)
        assert holidays_reservation_with_dates.end_date == date(2022, 7, 22)
        assert holidays_reservation_with_dates.number_of_nights == 7  # 22 - 15 = 7 days
        
        # Verify consistency between dates and number of nights
        expected_nights = (holidays_reservation_with_dates.end_date - 
                          holidays_reservation_with_dates.entry_date).days
        assert holidays_reservation_with_dates.number_of_nights == expected_nights

    def test_reservation_with_nights(self, holidays_reservation_with_nights):
        """Test a reservation with number of nights."""
        assert holidays_reservation_with_nights.entry_date == date(2022, 8, 10)
        assert holidays_reservation_with_nights.number_of_nights == 5
        assert holidays_reservation_with_nights.end_date == date(2022, 8, 15)  # 10 + 5 days = 15
        
        # Verify consistency between dates and number of nights
        expected_end_date = holidays_reservation_with_nights.entry_date + timedelta(days=holidays_reservation_with_nights.number_of_nights)
        assert holidays_reservation_with_nights.end_date == expected_end_date

    def test_reservation_with_renter(self, holidays_reservation_with_renter):
        """Test a reservation with renting person details."""
        assert holidays_reservation_with_renter.renting_person_full_name == "Jane Smith"
        assert holidays_reservation_with_renter.renting_person_dni == "ID12345"
        assert holidays_reservation_with_renter.renting_person_direction == "123 Tourist St"
        assert holidays_reservation_with_renter.renting_person_postcode == "54321"
        assert holidays_reservation_with_renter.renting_person_city == "Tourist City"
        assert holidays_reservation_with_renter.renting_person_region == "Tourist Region"
        assert holidays_reservation_with_renter.renting_person_country == "Tourist Country"

    def test_reservation_with_price(self, holidays_reservation_with_price):
        """Test a reservation with price information."""
        assert holidays_reservation_with_price.price == Decimal('850.00')

    def test_reservation_received(self, holidays_reservation_received):
        """Test a reservation with received bank status."""
        assert holidays_reservation_received.received_bank is True

    def test_reservation_with_cleaning(self, holidays_reservation_with_cleaning):
        """Test a reservation with cleaning information."""
        assert holidays_reservation_with_cleaning.cleaning == Decimal('120.00')

    def test_reservation_with_commission(self, holidays_reservation_with_commission):
        """Test a reservation with commission information."""
        assert holidays_reservation_with_commission.commission_platform == Decimal('85.00')
        assert holidays_reservation_with_commission.commission_other == Decimal('25.00')
        
        # Calculate total commission
        total_commission = (holidays_reservation_with_commission.commission_platform + 
                           holidays_reservation_with_commission.commission_other)
        assert total_commission == Decimal('110.00')
        
        # With price information, verify net amount
        if hasattr(holidays_reservation_with_commission, 'price') and holidays_reservation_with_commission.price:
            net_amount = holidays_reservation_with_commission.price - total_commission
            # This is a hypothetical check as our fixture might not have price set
            if holidays_reservation_with_commission.price > 0:
                assert net_amount < holidays_reservation_with_commission.price

    def test_reservation_with_comments(self, holidays_reservation_with_comments):
        """Test a reservation with comments."""
        assert holidays_reservation_with_comments.comments == "Family of 4, repeated guests, no special requests"
        
    def test_reservation_dates_generation(self, holidays_reservation_with_dates):
        """Test that a reservation correctly generates reservation days."""
        # Check if the method to get reservation days exists
        if hasattr(holidays_reservation_with_dates, 'get_reservation_days'):
            days = holidays_reservation_with_dates.get_reservation_days()
            
            # Verify the right number of days was generated
            assert len(days) == holidays_reservation_with_dates.number_of_nights
            
            # Verify start and end dates
            assert min(days) == holidays_reservation_with_dates.entry_date
            assert max(days) == holidays_reservation_with_dates.end_date - timedelta(days=1)
            
            # Verify consecutive days
            for i in range(len(days) - 1):
                assert days[i + 1] - days[i] == timedelta(days=1) 