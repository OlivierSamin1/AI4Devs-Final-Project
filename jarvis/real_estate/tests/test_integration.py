"""
Integration tests for the real_estate app.
These tests verify the interactions between different models.
"""
import pytest
from datetime import date, timedelta
from django.contrib.auth import get_user_model

from real_estate.models import (
    Asset,
    Bill,
    Mortgage,
    Tenant,
    CoproManagementCompany,
    CoproManagementContract,
    RentingManagementCompany,
    RentingManagementContract,
    UtilitySupplier,
    UtilityContract,
    HollydaysPlatform,
    HollydaysReservation,
    FileAsset,
    FileBill,
    FileMortgage,
    FileTenant,
    FileCoPro,
    FileRenting,
    FileUtility,
    FileHollyDaysPlatform,
    FileHollyDaysReservation
)
from .factories import (
    AssetFactory,
    BillFactory,
    MortgageFactory,
    TenantFactory,
    CoproManagementContractFactory,
    RentingManagementContractFactory,
    UtilityContractFactory,
    HollydaysReservationFactory,
    FileAssetFactory,
    FileBillFactory,
    FileMortgageFactory,
    FileTenantFactory
)

User = get_user_model()


@pytest.mark.django_db
class TestRealEstateIntegration:
    """Integration tests for the real_estate app models."""
    
    def test_asset_with_mortgage_relation(self, user):
        """Test an asset with a mortgage relation."""
        # Arrange
        asset = Asset.objects.create(
            owner=user,
            nickname="Property with Mortgage",
            address="123 Test Street",
            postal_code=12345,
            city="Test City",
            country="Test Country",
            has_on_going_mortgage=True,
            details={"type": "apartment"},
            results_by_year={"2022": {"income": 0, "expenses": 0}}
        )
        mortgage = Mortgage.objects.create(
            asset=asset,
            name="Primary Mortgage",
            starting_date=date.today() - timedelta(days=365),
            ending_date=date.today() + timedelta(days=3650),
            rate_renegociations={"2022": "2.1%"},
            annual_interests={"2022": 4500},
            annual_capital_refund={"2022": 6000},
            capital_due_end_of_year={"2022": 194000}
        )
        
        # Act
        # Query the asset's mortgage
        asset_mortgage = asset.mortgage
        
        # Assert
        assert asset_mortgage is not None
        assert asset_mortgage.name == "Primary Mortgage"
        assert asset_mortgage.asset == asset
        assert asset.has_on_going_mortgage is True
    
    def test_asset_with_tenant_relation(self, user):
        """Test an asset with a tenant relation."""
        # Arrange
        asset1 = Asset.objects.create(
            owner=user,
            nickname="Rental Property 1",
            address="456 Tenant Street",
            postal_code=54321,
            city="Rental City",
            country="Rental Country",
            is_rented=True,
            details={"type": "house"},
            results_by_year={"2022": {"income": 12000, "expenses": 3000}}
        )
        asset2 = Asset.objects.create(
            owner=user,
            nickname="Rental Property 2",
            address="789 Tenant Avenue",
            postal_code=54322,
            city="Rental City",
            country="Rental Country",
            is_rented=True,
            details={"type": "apartment"},
            results_by_year={"2022": {"income": 10000, "expenses": 2500}}
        )
        tenant1 = Tenant.objects.create(
            asset=asset1,
            first_name="John",
            last_name="Doe",
            phone_number=600000001,
            email="john.doe@example.com",
            id_type="passport",
            id_number="AB123456",
            is_actual_tenant=True,
            comments={"notes": "Good tenant"}
        )
        tenant2 = Tenant.objects.create(
            asset=asset2,
            first_name="Jane",
            last_name="Smith",
            phone_number=600000002,
            email="jane.smith@example.com",
            id_type="dni",
            id_number="CD789012",
            is_actual_tenant=True,
            comments={"notes": "Pays on time"}
        )
        
        # Act
        # Query all tenants for the user's assets
        user_assets = Asset.objects.filter(owner=user, is_rented=True)
        tenants = Tenant.objects.filter(asset__in=user_assets)
        
        # Assert
        assert tenants.count() == 2
        assert any(t.first_name == "John" and t.last_name == "Doe" for t in tenants)
        assert any(t.first_name == "Jane" and t.last_name == "Smith" for t in tenants)
        assert asset1.is_rented is True
        assert asset2.is_rented is True
    
    def test_asset_with_bills(self, user):
        """Test an asset with related bills."""
        # Arrange
        asset = Asset.objects.create(
            owner=user,
            nickname="Property with Bills",
            address="789 Bill Street",
            postal_code=98765,
            city="Bill City",
            country="Bill Country",
            details={"type": "condo"},
            results_by_year={"2022": {"income": 0, "expenses": 5000}}
        )
        bill1 = Bill.objects.create(
            asset=asset,
            company_name="Electric Company",
            client_name=user,
            bill_name="Electricity",
            date=date(2023, 1, 15),
            total_price=150.0,
            tax=30.0,
            price_without_tax=120.0
        )
        bill2 = Bill.objects.create(
            asset=asset,
            company_name="Water Services",
            client_name=user,
            bill_name="Water",
            date=date(2023, 2, 20),
            total_price=75.0,
            tax=15.0,
            price_without_tax=60.0
        )
        bill3 = Bill.objects.create(
            asset=asset,
            company_name="Internet Provider",
            client_name=user,
            bill_name="Internet",
            date=date(2023, 3, 10),
            total_price=60.0,
            tax=12.0,
            price_without_tax=48.0
        )
        
        # Act
        # Query all bills for the asset
        bills = Bill.objects.filter(asset=asset).order_by('date')
        
        # Assert
        assert bills.count() == 3
        assert bills[0].bill_name == "Electricity"
        assert bills[1].bill_name == "Water"
        assert bills[2].bill_name == "Internet"
        
        # Test total expenses
        total_expenses = sum(bill.total_price for bill in bills)
        assert total_expenses == 285.0  # 150 + 75 + 60
    
    def test_asset_with_copro_management(self, user):
        """Test an asset with copro management."""
        # Arrange
        asset = Asset.objects.create(
            owner=user,
            nickname="Managed Condo",
            address="101 Copro Ave",
            postal_code=13579,
            city="Copro City",
            country="Copro Country",
            details={"type": "apartment"},
            results_by_year={"2022": {"income": 0, "expenses": 1500}}
        )
        company = CoproManagementCompany.objects.create(
            name="Copro Management Inc",
            personal_email_used="contact@copromanagement.com",
            site_app_company="copromanagement.com"
        )
        copro_contract = CoproManagementContract.objects.create(
            company=company,
            contract_number="CM-12345",
            asset=asset,
            starting_date=date.today() - timedelta(days=365),
            ending_date=date.today() + timedelta(days=365),
            is_management_active=True,
            monthly_price=120.50,
            year=date.today().year,
            annual_expenses={
                str(date.today().year - 1): {
                    "fixed": 1200,
                    "refurbishment": 300
                }
            }
        )
        
        # Act
        # Set the contract on the asset
        asset.copro_contract = copro_contract
        asset.save()
        
        # Refresh from db
        asset.refresh_from_db()
        
        # Assert
        assert asset.copro_contract is not None
        assert asset.copro_contract.monthly_price == 120.50
        assert asset.copro_contract.is_management_active is True
        
        # Test the reverse relation
        assert copro_contract.asset_copro_contract == asset
    
    def test_asset_with_renting_management(self, user):
        """Test an asset with renting management."""
        # Arrange
        asset = Asset.objects.create(
            owner=user,
            nickname="Managed Rental",
            address="202 Rental Blvd",
            postal_code=24680,
            city="Rental City",
            country="Rental Country",
            is_rented=True,
            details={"type": "house"},
            results_by_year={"2022": {"income": 12000, "expenses": 4000}}
        )
        company = RentingManagementCompany.objects.create(
            name="Rental Management LLC",
            personal_email_used="contact@rentalmanagement.com",
            site_app_company="rentalmanagement.com"
        )
        renting_contract = RentingManagementContract.objects.create(
            company=company,
            contract_number="RM-67890",
            asset=asset,
            starting_date=date.today() - timedelta(days=365),
            ending_date=date.today() + timedelta(days=365),
            is_management_active=True,
            annual_results={
                str(date.today().year - 1): {
                    "income": 12000,
                    "expenses": 4000,
                    "profit": 8000
                }
            }
        )
        
        # Act
        # Set the contract on the asset
        asset.renting_contract = renting_contract
        asset.save()
        
        # Refresh from db
        asset.refresh_from_db()
        
        # Assert
        assert asset.renting_contract is not None
        assert asset.renting_contract.is_management_active is True
        assert asset.is_rented is True
        
        # Test the reverse relation
        assert renting_contract.asset_renting_contract == asset
    
    def test_asset_with_utility_contracts(self, user):
        """Test an asset with utility contracts."""
        # Arrange
        asset = Asset.objects.create(
            owner=user,
            nickname="Utility Property",
            address="303 Utility Road",
            postal_code=36925,
            city="Utility City",
            country="Utility Country",
            details={"type": "apartment"},
            results_by_year={"2022": {"income": 0, "expenses": 2200}}
        )
        supplier = UtilitySupplier.objects.create(
            name="Multi Utility Provider",
            personal_email_used="contact@utility.com",
            phone="600123456"
        )
        electricity_contract = UtilityContract.objects.create(
            supplier=supplier,
            user=user,
            asset=asset,
            service="Electricity",
            contract_number="UTL-E12345",
            monthly_price=85.0,
            is_active=True
        )
        water_contract = UtilityContract.objects.create(
            supplier=supplier,
            user=user,
            asset=asset,
            service="Water",
            contract_number="UTL-W12345",
            monthly_price=45.0,
            is_active=True
        )
        internet_contract = UtilityContract.objects.create(
            supplier=supplier,
            user=user,
            asset=asset,
            service="Internet",
            contract_number="UTL-I12345",
            monthly_price=55.0,
            is_active=True
        )
        
        # Act
        # Query all utility contracts for the asset
        utility_contracts = UtilityContract.objects.filter(asset=asset)
        
        # Assert
        assert utility_contracts.count() == 3
        
        # Test services covered
        services = [contract.service for contract in utility_contracts]
        assert "Electricity" in services
        assert "Water" in services
        assert "Internet" in services
        
        # Test total monthly utilities cost
        total_monthly_cost = sum(contract.monthly_price for contract in utility_contracts)
        assert total_monthly_cost == 185.0  # 85 + 45 + 55
    
    def test_asset_with_holiday_reservations(self, user):
        """Test an asset with holiday reservations."""
        # Arrange
        asset = Asset.objects.create(
            owner=user,
            nickname="Holiday Home",
            address="404 Beach Front",
            postal_code=11223,
            city="Beach City",
            country="Beach Country",
            details={"type": "vacation_home"},
            results_by_year={"2022": {"income": 15000, "expenses": 5000}}
        )
        platform = HollydaysPlatform.objects.create(
            name="Holiday Rentals",
            personal_email_used="contact@holidayrentals.com",
            site_app_company="holidayrentals.com"
        )
        today = date.today()
        
        # Create reservations for different periods
        reservation1 = HollydaysReservation.objects.create(
            platform=platform,
            asset=asset,
            reservation_number="RES-001",
            entry_date=today + timedelta(days=10),
            number_of_nights=5,
            end_date=today + timedelta(days=15),
            renting_person_full_name="Alice Johnson",
            price=750.0
        )
        reservation2 = HollydaysReservation.objects.create(
            platform=platform,
            asset=asset,
            reservation_number="RES-002",
            entry_date=today + timedelta(days=20),
            number_of_nights=7,
            end_date=today + timedelta(days=27),
            renting_person_full_name="Bob Smith",
            price=1050.0
        )
        reservation3 = HollydaysReservation.objects.create(
            platform=platform,
            asset=asset,
            reservation_number="RES-003",
            entry_date=today + timedelta(days=35),
            number_of_nights=3,
            end_date=today + timedelta(days=38),
            renting_person_full_name="Carol Davis",
            price=450.0
        )
        
        # Act
        # Query all holiday reservations for the asset
        reservations = HollydaysReservation.objects.filter(asset=asset).order_by('entry_date')
        
        # Assert
        assert reservations.count() == 3
        
        # Verify chronological order
        assert reservations[0].entry_date == today + timedelta(days=10)
        assert reservations[1].entry_date == today + timedelta(days=20)
        assert reservations[2].entry_date == today + timedelta(days=35)
        
        # Verify end dates are calculated correctly
        assert reservations[0].end_date == today + timedelta(days=15)  # entry_date + 5 nights
        assert reservations[1].end_date == today + timedelta(days=27)  # entry_date + 7 nights
        assert reservations[2].end_date == today + timedelta(days=38)  # entry_date + 3 nights
        
        # Verify total income from reservations
        total_income = sum(reservation.price for reservation in reservations)
        assert total_income == 2250.0  # 750 + 1050 + 450
    
    def test_asset_with_files(self, user):
        """Test an asset with related files."""
        # Arrange
        asset = Asset.objects.create(
            owner=user,
            nickname="Documentation Property",
            address="505 Document Way",
            postal_code=55443,
            city="Doc City",
            country="Doc Country",
            details={"type": "house"},
            results_by_year={"2022": {"income": 0, "expenses": 0}}
        )
        # Create test files directly instead of using factory
        file1 = FileAsset.objects.create(
            access_to_model=asset,
            name="Property Deed"
        )
        file2 = FileAsset.objects.create(
            access_to_model=asset,
            name="Floor Plan"
        )
        file3 = FileAsset.objects.create(
            access_to_model=asset,
            name="Property Photos"
        )
        
        # Act
        # Query all files for the asset
        files = FileAsset.objects.filter(access_to_model=asset)
        
        # Assert
        assert files.count() == 3
        file_names = [file.name for file in files]
        assert "Property Deed" in file_names
        assert "Floor Plan" in file_names
        assert "Property Photos" in file_names 