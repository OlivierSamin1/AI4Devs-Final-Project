"""
Integration tests for the administrative app.
These tests verify interactions between different components.
"""
import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from django.utils import timezone
import os

from administrative.models import (
    Document,
    InsuranceCompany,
    InsuranceContract,
    File,
    FileDocument,
    FileInsuranceContract
)
from .factories import (
    UserFactory,
    DocumentFactory,
    InsuranceCompanyFactory,
    InsuranceContractFactory,
    FileDocumentFactory,
    FileInsuranceContractFactory
)

User = get_user_model()


@pytest.mark.django_db
class TestInsuranceAndDocumentsIntegration:
    """Integration tests for insurance and document models."""

    def test_user_with_documents_and_insurance(self):
        """Test a user with multiple documents and insurance contracts."""
        # Arrange
        user = UserFactory()
        
        # Create documents
        doc1 = DocumentFactory(user=user, type="ID card")
        doc2 = DocumentFactory(user=user, type="Passport")
        
        # Create insurance company and contracts
        company = InsuranceCompanyFactory()
        contract1 = InsuranceContractFactory(
            company=company,
            type="Person insurance",
            person=user
        )
        contract2 = InsuranceContractFactory(
            company=company,
            type="Real Estate insurance",
            person=user
        )
        
        # Act
        user_documents = Document.objects.filter(user=user)
        user_insurance = InsuranceContract.objects.filter(person=user)
        
        # Assert
        assert user_documents.count() == 2
        assert user_insurance.count() == 2
        assert any(doc.type == "ID card" for doc in user_documents)
        assert any(contract.type == "Person insurance" for contract in user_insurance)
    
    def test_document_with_multiple_files(self):
        """Test a document with multiple attached files."""
        # Arrange
        document = DocumentFactory()
        file1 = FileDocumentFactory(access_to_model=document, name="Front page")
        file2 = FileDocumentFactory(access_to_model=document, name="Back page")
        
        # Act
        document_files = FileDocument.objects.filter(access_to_model=document)
        
        # Assert
        assert document_files.count() == 2
        assert any(file.name == "Front page" for file in document_files)
        assert any(file.name == "Back page" for file in document_files)
    
    def test_contract_with_multiple_files(self):
        """Test an insurance contract with multiple attached files."""
        # Arrange
        contract = InsuranceContractFactory()
        file1 = FileInsuranceContractFactory(access_to_model=contract, name="Terms and conditions")
        file2 = FileInsuranceContractFactory(access_to_model=contract, name="Coverage details")
        
        # Act
        contract_files = FileInsuranceContract.objects.filter(access_to_model=contract)
        
        # Assert
        assert contract_files.count() == 2
        assert any(file.name == "Terms and conditions" for file in contract_files)
        assert any(file.name == "Coverage details" for file in contract_files)
    
    def test_company_with_multiple_contracts(self):
        """Test an insurance company with multiple contracts."""
        # Arrange
        company = InsuranceCompanyFactory()
        user1 = UserFactory()
        user2 = UserFactory()
        
        contract1 = InsuranceContractFactory(company=company, person=user1, type="Person insurance")
        contract2 = InsuranceContractFactory(company=company, person=user2, type="Person insurance")
        contract3 = InsuranceContractFactory(company=company, person=user1, type="Real Estate insurance")
        
        # Act
        company_contracts = InsuranceContract.objects.filter(company=company)
        user1_contracts = InsuranceContract.objects.filter(person=user1)
        user2_contracts = InsuranceContract.objects.filter(person=user2)
        
        # Assert
        assert company_contracts.count() == 3
        assert user1_contracts.count() == 2
        assert user2_contracts.count() == 1
    
    def test_document_cascade_delete(self):
        """Test that when a document is deleted, its files are also deleted from database."""
        # Arrange
        document = DocumentFactory()
        file1 = FileDocumentFactory(access_to_model=document)
        file2 = FileDocumentFactory(access_to_model=document)
        
        file_ids = [file1.id, file2.id]
        
        # Act
        document.delete()
        
        # Assert
        # Files should be deleted from database
        assert not FileDocument.objects.filter(id__in=file_ids).exists()
        # Note: Physical file deletion would require custom delete handling in the model
    
    def test_contract_cascade_delete(self):
        """Test that when a contract is deleted, its files are also deleted from database."""
        # Arrange
        contract = InsuranceContractFactory()
        file1 = FileInsuranceContractFactory(access_to_model=contract)
        file2 = FileInsuranceContractFactory(access_to_model=contract)
        
        file_ids = [file1.id, file2.id]
        
        # Act
        contract.delete()
        
        # Assert
        # Files should be deleted from database
        assert not FileInsuranceContract.objects.filter(id__in=file_ids).exists()
        # Note: Physical file deletion would require custom delete handling in the model
    
    def test_company_cascade_delete(self):
        """Test that when a company is deleted, its contracts are also deleted."""
        # Arrange
        company = InsuranceCompanyFactory()
        contract1 = InsuranceContractFactory(company=company)
        contract2 = InsuranceContractFactory(company=company)
        
        contract_ids = [contract1.id, contract2.id]
        
        # Act
        company.delete()
        
        # Assert
        # Contracts should be deleted
        assert not InsuranceContract.objects.filter(id__in=contract_ids).exists()
    
    def test_user_with_documents_and_files(self):
        """Test retrieving all documents and files for a user."""
        # Arrange
        user = UserFactory()
        doc1 = DocumentFactory(user=user)
        doc2 = DocumentFactory(user=user)
        
        file1 = FileDocumentFactory(access_to_model=doc1)
        file2 = FileDocumentFactory(access_to_model=doc1)
        file3 = FileDocumentFactory(access_to_model=doc2)
        
        # Act
        user_documents = Document.objects.filter(user=user)
        document_ids = user_documents.values_list('id', flat=True)
        user_files = FileDocument.objects.filter(access_to_model_id__in=document_ids)
        
        # Assert
        assert user_documents.count() == 2
        assert user_files.count() == 3
    
    def test_complex_user_insurance_relationship(self):
        """Test complex relationship between users and insurance contracts."""
        # Arrange
        user1 = UserFactory()
        user2 = UserFactory()
        
        company1 = InsuranceCompanyFactory(name="Company A")
        company2 = InsuranceCompanyFactory(name="Company B")
        
        # User1 has contracts with both companies
        contract1 = InsuranceContractFactory(company=company1, person=user1, type="Person insurance")
        contract2 = InsuranceContractFactory(company=company2, person=user1, type="Real Estate insurance")
        
        # User2 has contract with company1 only
        contract3 = InsuranceContractFactory(company=company1, person=user2, type="Person insurance")
        
        # Act
        user1_contracts = InsuranceContract.objects.filter(person=user1)
        user2_contracts = InsuranceContract.objects.filter(person=user2)
        company1_contracts = InsuranceContract.objects.filter(company=company1)
        company2_contracts = InsuranceContract.objects.filter(company=company2)
        
        # Assert
        assert user1_contracts.count() == 2
        assert user2_contracts.count() == 1
        assert company1_contracts.count() == 2
        assert company2_contracts.count() == 1
        
        # Check if User1 has contracts with both companies
        user1_companies = set(user1_contracts.values_list('company__name', flat=True))
        assert user1_companies == {"Company A", "Company B"}
        
        # Check if Company1 has contracts with both users
        company1_persons = set(company1_contracts.values_list('person_id', flat=True))
        assert len(company1_persons) == 2
        assert user1.id in company1_persons
        assert user2.id in company1_persons


@pytest.mark.django_db
class TestCrossModelValidations:
    """Integration tests for validations across multiple models."""
    
    def test_unique_document_type_per_user(self):
        """Test unique constraint on document type per user."""
        # In a real app, you might have a unique_together constraint on (user, type)
        # Here we're just testing the concept
        
        # Arrange
        user = UserFactory()
        DocumentFactory(user=user, type="Passport", name="Original Passport")
        
        # Act & Assert
        # No error expected for different types
        DocumentFactory(user=user, type="ID card")
        
        # No error expected for same type but different user
        other_user = UserFactory()
        DocumentFactory(user=other_user, type="Passport")
        
        # In a real app with a unique_together constraint, this would fail
        # For this test, we're just demonstrating the concept
        duplicate = DocumentFactory(user=user, type="Passport", name="Second Passport")
        assert duplicate.id is not None
    
    def test_document_file_relationship_integrity(self):
        """Test that files properly reference their documents."""
        # Arrange
        document = DocumentFactory()
        file = FileDocumentFactory(access_to_model=document)
        
        # Act
        loaded_document = Document.objects.get(id=document.id)
        loaded_file = FileDocument.objects.get(id=file.id)
        
        # Assert
        assert loaded_file.access_to_model.id == loaded_document.id
        assert loaded_file.access_to_model == loaded_document
    
    def test_contract_file_relationship_integrity(self):
        """Test that files properly reference their contracts."""
        # Arrange
        contract = InsuranceContractFactory()
        file = FileInsuranceContractFactory(access_to_model=contract)
        
        # Act
        loaded_contract = InsuranceContract.objects.get(id=contract.id)
        loaded_file = FileInsuranceContract.objects.get(id=file.id)
        
        # Assert
        assert loaded_file.access_to_model.id == loaded_contract.id
        assert loaded_file.access_to_model == loaded_contract
    
    def test_cross_model_file_reference(self):
        """Test that file objects reference the correct model types."""
        # Arrange
        document = DocumentFactory()
        contract = InsuranceContractFactory()
        
        # Act & Assert
        # These should succeed
        file_doc = FileDocumentFactory(access_to_model=document)
        assert file_doc.id is not None
        
        file_contract = FileInsuranceContractFactory(access_to_model=contract)
        assert file_contract.id is not None
        
        # Note: In a more strictly typed system, we would test that a FileDocument
        # cannot reference an insurance contract and vice versa, but Django's
        # ForeignKey doesn't enforce this at the database level 


@pytest.mark.django_db
class TestAdvancedIntegrationScenarios:
    """Advanced integration tests for complex business scenarios."""
    
    def test_contract_type_migration(self):
        """Test changing contract type and related assets."""
        # Arrange
        company = InsuranceCompanyFactory()
        user = UserFactory()
        
        # Create a person insurance contract
        contract = InsuranceContractFactory(
            company=company,
            type="Person insurance",
            person=user,
            annual_price={"2023": 300},
            coverage={"health": "full"}
        )
        
        # Create some contract files
        file1 = FileInsuranceContractFactory(access_to_model=contract, name="Original terms")
        
        # Act - Migrate to a different type
        # In a real application, this might involve more logic and asset validations
        contract.type = "Real Estate insurance"
        contract.coverage = {"property": "full", "liability": "full"}
        contract.annual_price = {"2023": 400}
        # We'd set real_estate_asset here in a real app
        contract.save()
        
        # Add a new file specific to the new contract type
        file2 = FileInsuranceContractFactory(access_to_model=contract, name="Property coverage")
        
        # Assert
        updated_contract = InsuranceContract.objects.get(id=contract.id)
        contract_files = FileInsuranceContract.objects.filter(access_to_model=contract)
        
        assert updated_contract.type == "Real Estate insurance"
        assert "property" in updated_contract.coverage
        assert updated_contract.annual_price["2023"] == 400
        assert contract_files.count() == 2
        assert any(file.name == "Original terms" for file in contract_files)
        assert any(file.name == "Property coverage" for file in contract_files)
    
    def test_document_lifecycle(self):
        """Test full document lifecycle: creation, update, attach files, deletion."""
        # Arrange
        user = UserFactory()
        
        # Act - Create document
        document = DocumentFactory(
            user=user,
            name="Initial Document",
            type="ID card",
            comment={"status": "new"}
        )
        
        # Assert initial state
        assert document.id is not None
        assert document.name == "Initial Document"
        
        # Act - Update document
        document.name = "Updated Document"
        document.comment = {"status": "updated", "updated_at": "2023-01-01"}
        document.save()
        
        # Assert updated state
        updated_document = Document.objects.get(id=document.id)
        assert updated_document.name == "Updated Document"
        assert updated_document.comment["status"] == "updated"
        
        # Act - Attach files
        file1 = FileDocumentFactory(access_to_model=document, name="First file")
        file2 = FileDocumentFactory(access_to_model=document, name="Second file")
        
        # Assert files are attached
        document_files = FileDocument.objects.filter(access_to_model=document)
        assert document_files.count() == 2
        
        # Act - Delete document and check cascade
        file_ids = [file1.id, file2.id]
        document.delete()
        
        # Assert document and files are deleted
        assert not Document.objects.filter(id=document.id).exists()
        assert not FileDocument.objects.filter(id__in=file_ids).exists()
    
    def test_insurance_lifecycle(self):
        """Test full insurance lifecycle: company creation, contracts, files, deletion."""
        # Arrange
        user = UserFactory()
        
        # Act - Create company
        company = InsuranceCompanyFactory(
            name="Lifecycle Insurance Co",
            phone_number=5551234567,
            site_app_company="www.lifecycle-insurance.com"
        )
        
        # Assert company created
        assert company.id is not None
        assert company.name == "Lifecycle Insurance Co"
        
        # Act - Create contracts
        contract1 = InsuranceContractFactory(
            company=company,
            type="Person insurance",
            person=user,
            coverage={"health": "full"}
        )
        
        contract2 = InsuranceContractFactory(
            company=company,
            type="Real Estate insurance",
            coverage={"property": "full"}
        )
        
        # Assert contracts created
        company_contracts = InsuranceContract.objects.filter(company=company)
        assert company_contracts.count() == 2
        
        # Act - Attach files to contracts
        file1 = FileInsuranceContractFactory(access_to_model=contract1, name="Health policy")
        file2 = FileInsuranceContractFactory(access_to_model=contract2, name="Property policy")
        
        # Assert files attached
        assert FileInsuranceContract.objects.filter(access_to_model=contract1).count() == 1
        assert FileInsuranceContract.objects.filter(access_to_model=contract2).count() == 1
        
        # Act - Update company
        company.name = "Renamed Insurance Co"
        company.save()
        
        # Assert company updated and relationships preserved
        updated_company = InsuranceCompany.objects.get(id=company.id)
        updated_contracts = InsuranceContract.objects.filter(company=updated_company)
        
        assert updated_company.name == "Renamed Insurance Co"
        assert updated_contracts.count() == 2
        
        # Act - Delete company and check cascade
        contract_ids = [contract1.id, contract2.id]
        file_ids = [file1.id, file2.id]
        company.delete()
        
        # Assert company, contracts, and files are deleted
        assert not InsuranceCompany.objects.filter(id=company.id).exists()
        assert not InsuranceContract.objects.filter(id__in=contract_ids).exists()
        assert not FileInsuranceContract.objects.filter(id__in=file_ids).exists()
    
    def test_cross_referenced_assets(self):
        """Test asset referenced by multiple contracts."""
        # Arrange
        company = InsuranceCompanyFactory()
        user = UserFactory()
        
        # Act - Create two contracts referencing the same entities
        contract1 = InsuranceContractFactory(
            company=company,
            type="Person insurance",
            person=user,
            coverage={"health": "basic"}
        )
        
        contract2 = InsuranceContractFactory(
            company=company,
            type="Person insurance",
            person=user,  # Same user
            coverage={"accident": "full"}
        )
        
        # Assert both contracts reference the same person
        assert contract1.person.id == contract2.person.id
        
        # In a real app, we would test with real assets like real estate or transportation
        # Since we don't have those models in this test, we're using person as the shared asset
        
        # Act - Update shared asset (user in this case)
        # In a real scenario, this could be updating a property address that affects multiple policies
        user.email = "updated@example.com"
        user.save()
        
        # Assert the change affects both contracts
        updated_user = User.objects.get(id=user.id)
        contracts_for_user = InsuranceContract.objects.filter(person=updated_user)
        
        assert contracts_for_user.count() == 2
        assert all(c.person.email == "updated@example.com" for c in contracts_for_user)
    
    def test_contract_renewal_with_history(self):
        """Test contract renewal while preserving history."""
        # Arrange
        company = InsuranceCompanyFactory()
        start_date = timezone.now().date()
        end_date = start_date + timezone.timedelta(days=365)
        
        # Create original contract
        original_contract = InsuranceContractFactory(
            company=company,
            type="Real Estate insurance",
            contract_number="RE-2023-001",
            starting_date=start_date,
            ending_date=end_date,
            annual_price={"2023": 400},
            coverage={"fire": "full", "flood": "partial"}
        )
        
        # Add a file to the original contract
        original_file = FileInsuranceContractFactory(
            access_to_model=original_contract,
            name="Original policy document"
        )
        
        # Act - Create renewal contract
        # In a real app, this might be handled by a specialized service
        renewal_start_date = end_date + timezone.timedelta(days=1)
        renewal_end_date = renewal_start_date + timezone.timedelta(days=365)
        
        # Store previous contract reference in the coverage JSON field
        renewal_contract = InsuranceContractFactory(
            company=company,
            type=original_contract.type,
            contract_number="RE-2024-001",  # New number for the new year
            starting_date=renewal_start_date,
            ending_date=renewal_end_date,
            annual_price={"2024": 420},  # Slight price increase
            coverage={
                **original_contract.coverage,  # Include original coverage
                "meta": {
                    "renewal_of": original_contract.id,  # Store reference to previous contract
                    "previous_contract_number": original_contract.contract_number
                }
            }
        )
        
        # Add a file to the renewal, possibly referencing the original contract
        renewal_file = FileInsuranceContractFactory(
            access_to_model=renewal_contract,
            name="Renewal policy document"
        )
        
        # Assert
        assert renewal_contract.id != original_contract.id
        assert renewal_contract.starting_date > original_contract.ending_date
        assert renewal_contract.coverage["meta"]["renewal_of"] == original_contract.id
        assert renewal_contract.coverage["meta"]["previous_contract_number"] == "RE-2023-001"
        assert renewal_contract.type == original_contract.type
        assert "fire" in renewal_contract.coverage  # Original coverage preserved
        assert "flood" in renewal_contract.coverage  # Original coverage preserved
        assert renewal_contract.annual_price != original_contract.annual_price
        
        # Verify that both contracts have their own files
        original_files = FileInsuranceContract.objects.filter(access_to_model=original_contract)
        renewal_files = FileInsuranceContract.objects.filter(access_to_model=renewal_contract)
        
        assert original_files.count() == 1
        assert renewal_files.count() == 1
        assert original_files.first().name == "Original policy document"
        assert renewal_files.first().name == "Renewal policy document"
    
    def test_document_version_control(self):
        """Test document versioning with multiple files."""
        # Arrange
        user = UserFactory()
        
        # Act - Create original document
        document = DocumentFactory(
            user=user,
            name="Versioned Document",
            type="Contract",
            comment={"version": "1.0", "status": "draft"}
        )
        
        # Add initial version file
        file_v1 = FileDocumentFactory(
            access_to_model=document,
            name="Document v1.0"
            # Store version in document.comment instead
        )
        
        # Act - Update document to version 1.1 (draft revision)
        document.comment = {"version": "1.1", "status": "draft", "changes": "Minor revisions"}
        document.save()
        
        # Add revised version file
        file_v1_1 = FileDocumentFactory(
            access_to_model=document,
            name="Document v1.1"
        )
        
        # Act - Finalize to version 2.0
        document.comment = {"version": "2.0", "status": "final", "changes": "Major revision, finalized"}
        document.save()
        
        # Add final version file
        file_v2 = FileDocumentFactory(
            access_to_model=document,
            name="Document v2.0 (Final)"
        )
        
        # Assert
        updated_document = Document.objects.get(id=document.id)
        document_files = FileDocument.objects.filter(access_to_model=document).order_by('id')
        
        assert updated_document.comment["version"] == "2.0"
        assert updated_document.comment["status"] == "final"
        
        # Verify all version files exist
        assert document_files.count() == 3
        assert document_files[0].name == "Document v1.0"
        assert document_files[1].name == "Document v1.1"
        assert document_files[2].name == "Document v2.0 (Final)"
        
        # Verify file names correspond to document versions
        assert "1.0" in document_files[0].name
        assert "1.1" in document_files[1].name
        assert "2.0" in document_files[2].name 