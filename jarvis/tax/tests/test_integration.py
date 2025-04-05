"""
Integration tests for the tax app.
"""
import pytest
from django.db.models import Q
from django.core.exceptions import ValidationError

from tax.models import Tax, TaxManagementCompany, TaxManagementContract, FileTax, FileTaxManagement


@pytest.mark.django_db
class TestTaxIntegration:
    """Integration tests for the tax app."""

    def test_create_tax_with_management_company(self, tax_management_company):
        """Test creating a tax linked to a management company."""
        # Arrange
        company = tax_management_company

        # Act
        tax = Tax.objects.create(
            name="Property Tax 2022",
            tax_type="Real Estate tax",
            tax_management_company=company,
            yearly_price=500,
            personal_email_used="test@example.com",
            is_tax_management_company_used=True
        )

        # Assert
        assert tax.id is not None
        assert tax.tax_management_company == company
        assert tax.tax_management_company.id == company.id
        assert tax.tax_management_company.name == company.name

        # Test querying by management company
        queried_tax = Tax.objects.filter(tax_management_company=company).first()
        assert queried_tax is not None
        assert queried_tax.id == tax.id

    def test_create_tax_management_contract_with_company_and_query(self, tax_management_company):
        """Test creating a contract with a management company and querying."""
        # Arrange
        company = tax_management_company

        # Act
        contract = TaxManagementContract.objects.create(
            company=company,
            contract_number="TC-789012",
            starting_date="2022-01-01",
            ending_date="2023-12-31",
            is_contract_active=True,
            annual_price={"2022": 600, "2023": 650}
        )

        # Assert
        assert contract.id is not None
        assert contract.company == company
        
        # Test querying
        queried_contract = TaxManagementContract.objects.filter(company=company).first()
        assert queried_contract is not None
        assert queried_contract.id == contract.id
        assert queried_contract.company.id == company.id
        
        # Test complex query
        active_contracts = TaxManagementContract.objects.filter(
            company=company,
            is_contract_active=True
        )
        assert active_contracts.count() == 1
        assert active_contracts.first().id == contract.id

    def test_tax_with_files(self, tax_with_online_access):
        """Test adding files to a tax and querying them."""
        # Arrange
        tax = tax_with_online_access
        
        # Act
        file1 = FileTax.objects.create(
            access_to_model=tax,
            name="Tax Assessment",
            content=None  # No actual file data for test
        )
        
        file2 = FileTax.objects.create(
            access_to_model=tax,
            name="Tax Payment",
            content=None  # No actual file data for test
        )
        
        # Assert
        assert file1.id is not None
        assert file2.id is not None
        
        # Test querying files by tax
        tax_files = FileTax.objects.filter(access_to_model=tax)
        assert tax_files.count() == 2
        
        # Test retrieving tax from file
        retrieved_tax = tax_files.first().access_to_model
        assert retrieved_tax.id == tax.id
        assert retrieved_tax.name == tax.name

    def test_tax_management_contract_with_files(self, contract_with_dates):
        """Test adding files to a contract and querying them."""
        # Arrange
        contract = contract_with_dates
        
        # Act
        file1 = FileTaxManagement.objects.create(
            access_to_model=contract,
            name="Contract Document",
            content=None  # No actual file data for test
        )
        
        file2 = FileTaxManagement.objects.create(
            access_to_model=contract,
            name="Invoice",
            content=None  # No actual file data for test
        )
        
        # Assert
        assert file1.id is not None
        assert file2.id is not None
        
        # Test querying files by contract
        contract_files = FileTaxManagement.objects.filter(access_to_model=contract)
        assert contract_files.count() == 2
        
        # Test retrieving contract from file
        retrieved_contract = contract_files.first().access_to_model
        assert retrieved_contract.id == contract.id

    def test_complex_query_taxes_by_type_and_online_access(self, real_estate_tax, transportation_tax):
        """Test complex queries combining tax type and online access."""
        # Arrange - using fixtures
        
        # Create one more tax with different attributes
        Tax.objects.create(
            name="Business Tax",
            tax_type="Other tax",
            site_app=None,
            yearly_price=800
        )
        
        # Act & Assert
        # Query for real estate taxes
        real_estate_taxes = Tax.objects.filter(tax_type="Real Estate tax")
        assert real_estate_taxes.count() == 1
        assert real_estate_taxes.first().id == real_estate_tax.id
        
        # Query for taxes with online access (using site_app or personal_email_used)
        online_taxes = Tax.objects.filter(Q(site_app__isnull=False) | Q(personal_email_used__isnull=False))
        # Both real_estate_tax and transportation_tax have online access info
        assert online_taxes.count() >= 2
        
        # Complex query: real estate taxes with online access
        complex_query = Tax.objects.filter(
            tax_type="Real Estate tax"
        ).filter(Q(site_app__isnull=False) | Q(personal_email_used__isnull=False))
        assert complex_query.count() == 1
        assert complex_query.first().id == real_estate_tax.id
        
        # Complex OR query
        or_query = Tax.objects.filter(
            Q(tax_type="Real Estate tax") | Q(tax_type="Transportation tax")
        )
        assert or_query.count() >= 2
        assert set(or_query.values_list('id', flat=True)) >= {real_estate_tax.id, transportation_tax.id}

    def test_tax_management_company_with_multiple_contracts(self, tax_management_company):
        """Test a management company with multiple contracts."""
        # Arrange
        company = tax_management_company
        
        # Act
        contract1 = TaxManagementContract.objects.create(
            company=company,
            contract_number="TC-MULTI-1",
            starting_date="2021-01-01",
            ending_date="2021-12-31",
            is_contract_active=False,
            annual_price={"2021": 500}
        )
        
        contract2 = TaxManagementContract.objects.create(
            company=company,
            contract_number="TC-MULTI-2",
            starting_date="2022-01-01",
            ending_date="2022-12-31",
            is_contract_active=True,
            annual_price={"2022": 550}
        )
        
        contract3 = TaxManagementContract.objects.create(
            company=company,
            contract_number="TC-MULTI-3",
            starting_date="2023-01-01",
            ending_date="2023-12-31",
            is_contract_active=True,
            annual_price={"2023": 600}
        )
        
        # Assert
        # Query all contracts for the company
        company_contracts = TaxManagementContract.objects.filter(company=company)
        assert company_contracts.count() >= 3
        
        # Query active contracts
        active_contracts = company_contracts.filter(is_contract_active=True)
        assert active_contracts.count() >= 2
        
        # Query inactive contracts
        inactive_contracts = company_contracts.filter(is_contract_active=False)
        assert inactive_contracts.count() >= 1
        assert inactive_contracts.first().id == contract1.id
        
        # Query by year (contracts ending in 2022)
        year_2022_contracts = company_contracts.filter(ending_date__year=2022)
        assert year_2022_contracts.count() >= 1
        assert year_2022_contracts.first().id == contract2.id

    def test_complete_tax_management_flow(self, user):
        """Test the complete flow: company, contract, tax, files."""
        # Arrange & Act
        # 1. Create a tax management company
        company = TaxManagementCompany.objects.create(
            name="Full Flow Tax Services",
            personal_email_used="flow@example.com",
            site_app_company="flowtax.example.com",
            comments="Integrated test"
        )
        
        # 2. Create a contract with the company
        contract = TaxManagementContract.objects.create(
            company=company,
            contract_number="TC-FLOW-1",
            starting_date="2022-01-01",
            ending_date="2024-12-31",
            is_contract_active=True,
            annual_price={"2022": 550, "2023": 600, "2024": 650}
        )
        
        # 3. Create taxes managed by the company
        tax1 = Tax.objects.create(
            name="Property Tax Flow",
            tax_type="Real Estate tax",
            tax_management_company=company,
            yearly_price=1200,
            is_tax_management_company_used=True,
            personal_email_used="property@example.com"
        )
        
        tax2 = Tax.objects.create(
            name="Vehicle Tax Flow",
            tax_type="Transportation tax",
            tax_management_company=company,
            yearly_price=400,
            is_tax_management_company_used=True,
            site_app="vehicle.tax.gov"
        )
        
        # 4. Add files to the contract
        contract_file = FileTaxManagement.objects.create(
            access_to_model=contract,
            name="Master Contract",
            content=None  # No actual file data for test
        )
        
        # 5. Add files to the taxes
        tax1_file = FileTax.objects.create(
            access_to_model=tax1,
            name="Property Assessment",
            content=None  # No actual file data for test
        )
        
        tax2_file = FileTax.objects.create(
            access_to_model=tax2,
            name="Vehicle Registration",
            content=None  # No actual file data for test
        )
        
        # Assert
        # Verify company
        assert company.id is not None
        
        # Verify contract is linked to company
        saved_contract = TaxManagementContract.objects.get(id=contract.id)
        assert saved_contract.company.id == company.id
        
        # Verify taxes are linked to company
        saved_taxes = Tax.objects.filter(tax_management_company=company)
        assert saved_taxes.count() == 2
        
        # Verify files are linked to contract and taxes
        contract_files = FileTaxManagement.objects.filter(access_to_model=contract)
        assert contract_files.count() == 1
        assert contract_files.first().id == contract_file.id
        
        tax1_files = FileTax.objects.filter(access_to_model=tax1)
        assert tax1_files.count() == 1
        assert tax1_files.first().id == tax1_file.id
        
        tax2_files = FileTax.objects.filter(access_to_model=tax2)
        assert tax2_files.count() == 1
        assert tax2_files.first().id == tax2_file.id
        
        # Complex query: all files related to this company
        # Get all taxes for the company
        company_taxes = Tax.objects.filter(tax_management_company=company)
        # Get all files for those taxes
        tax_files = FileTax.objects.filter(access_to_model__in=company_taxes)
        # Get all contracts for the company
        company_contracts = TaxManagementContract.objects.filter(company=company)
        # Get all files for those contracts
        contract_files = FileTaxManagement.objects.filter(access_to_model__in=company_contracts)
        
        # Assert file counts
        assert tax_files.count() == 2
        assert contract_files.count() == 1 