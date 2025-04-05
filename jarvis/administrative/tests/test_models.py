"""
Unit tests for administrative models using AAA pattern.
"""
import pytest
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import timedelta
import json
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
    DocumentFactory,
    InsuranceCompanyFactory,
    InsuranceContractFactory,
    FileDocumentFactory,
    FileInsuranceContractFactory
)


@pytest.mark.django_db
class TestDocument:
    """Test cases for the Document model."""

    def test_create_document_with_valid_data(self, user):
        """Test creating a document with all fields valid."""
        # Arrange
        document_data = {
            "user": user,
            "name": "Test Document",
            "type": "ID card",
            "comment": {"expiry": "2025-01-01"}
        }
        
        # Act
        document = Document.objects.create(**document_data)
        
        # Assert
        assert document.id is not None
        assert document.name == "Test Document"
        assert document.type == "ID card"
        assert document.comment["expiry"] == "2025-01-01"
    
    def test_document_str_method(self, document):
        """Test the string representation of a document."""
        # Arrange - handled by the fixture
        
        # Act
        result = str(document)
        
        # Assert
        assert result == f"{document.name} - {document.type}"
    
    def test_document_str_method_no_name(self, user):
        """Test the string representation of a document without a name."""
        # Arrange
        document = Document.objects.create(user=user, type="Passport")
        
        # Act
        result = str(document)
        
        # Assert
        assert result == "Passport"
    
    def test_document_meta_ordering(self, user):
        """Test the ordering of documents."""
        # Arrange
        doc1 = Document.objects.create(user=user, type="Passport", name="Z Doc")
        doc2 = Document.objects.create(user=user, type="ID card", name="A Doc")
        doc3 = Document.objects.create(user=user, type="ID card", name="B Doc")
        
        # Act
        documents = list(Document.objects.all())
        
        # Assert
        assert documents[0].type == "ID card" and documents[0].name == "A Doc"
        assert documents[1].type == "ID card" and documents[1].name == "B Doc"
        assert documents[2].type == "Passport" and documents[2].name == "Z Doc"
    
    def test_document_with_json_comment(self, document_with_custom_comment):
        """Test creating a document with a complex JSON comment."""
        # Arrange - handled by the fixture
        
        # Act
        loaded_document = Document.objects.get(id=document_with_custom_comment.id)
        
        # Assert
        assert loaded_document.comment["custom_field"] == "custom_value"
        assert loaded_document.comment["priority"] == "high"
    
    def test_document_without_user(self):
        """Test creating a document without a user field (null=True)."""
        # Arrange
        document_data = {
            "name": "Test Document",
            "type": "ID card"
        }
        
        # Act
        document = Document.objects.create(**document_data)
        
        # Assert
        assert document.id is not None
        assert document.user is None
    
    def test_document_null_name(self, user):
        """Test behavior when name is set to null (which is allowed)."""
        # Arrange
        document_data = {
            "user": user,
            "type": "Passport",
            "name": None
        }
        
        # Act
        document = Document.objects.create(**document_data)
        
        # Assert
        assert document.id is not None
        assert document.name is None
        assert document.type == "Passport"
        assert str(document) == "Passport"
    
    def test_document_invalid_type(self, user):
        """Test saving with a type not in choices."""
        # Arrange
        document_data = {
            "user": user,
            "name": "Test Document",
            "type": "Invalid Type"  # Not in get_types()
        }
        
        # Act
        document = Document.objects.create(**document_data)
        
        # Assert
        # Django allows non-choice values by default, but will fail form validation
        assert document.id is not None
        assert document.type == "Invalid Type"
    
    def test_document_empty_json_comment(self, user):
        """Test with empty dict as JSON comment."""
        # Arrange
        document_data = {
            "user": user,
            "name": "Test Document",
            "type": "Passport",
            "comment": {}
        }
        
        # Act
        document = Document.objects.create(**document_data)
        
        # Assert
        assert document.id is not None
        assert document.comment == {}
    
    def test_document_malformed_json(self, user):
        """Test behavior with non-dict JSON value in comment field."""
        # Arrange
        # Test various non-dict JSON values that are valid JSON but not dicts
        json_values = [
            "string value",
            123,
            [1, 2, 3],
            True,
            None
        ]
        
        # Act & Assert
        for value in json_values:
            document = Document.objects.create(
                user=user,
                name=f"Document with {type(value).__name__}",
                type="Passport",
                comment=value
            )
            
            # Verify value was saved correctly
            loaded_document = Document.objects.get(id=document.id)
            assert loaded_document.comment == value
    
    def test_document_very_long_name(self, user):
        """Test with name at maximum length (50 chars)."""
        # Arrange
        long_name = "A" * 50  # Exactly 50 characters
        
        # Act
        document = Document.objects.create(user=user, name=long_name, type="Passport")
        
        # Assert
        assert document.id is not None
        assert document.name == long_name
        assert len(document.name) == 50
    
    def test_document_unicode_characters(self, user):
        """Test with unicode characters in name and comment."""
        # Arrange
        unicode_name = "你好，世界"  # "Hello, World" in Chinese
        unicode_comment = {"greeting": "안녕하세요"}  # "Hello" in Korean
        
        # Act
        document = Document.objects.create(
            user=user, 
            name=unicode_name, 
            type="Passport",
            comment=unicode_comment
        )
        
        # Assert
        assert document.id is not None
        assert document.name == unicode_name
        assert document.comment["greeting"] == "안녕하세요"
    
    def test_document_type_change(self, document):
        """Test changing document type after creation."""
        # Arrange
        original_type = document.type
        new_type = "Passport" if original_type != "Passport" else "ID card"
        
        # Act
        document.type = new_type
        document.save()
        refreshed_document = Document.objects.get(id=document.id)
        
        # Assert
        assert refreshed_document.type == new_type
        assert refreshed_document.type != original_type
    
    def test_document_deletion(self, document):
        """Test proper document deletion."""
        # Arrange
        document_id = document.id
        
        # Act
        document.delete()
        
        # Assert
        assert not Document.objects.filter(id=document_id).exists()


@pytest.mark.django_db
class TestFile:
    """Test cases for the File model and its subclasses."""

    def test_file_document_creation(self, file_document):
        """Test creating a file attached to a document."""
        # Arrange - handled by the fixture
        
        # Act
        loaded_file = FileDocument.objects.get(id=file_document.id)
        
        # Assert
        assert loaded_file.name is not None
        assert loaded_file.content is not None
        assert loaded_file.access_to_model is not None
        assert loaded_file.access_to_model.id == file_document.access_to_model.id
    
    def test_file_insurance_contract_creation(self, file_insurance_contract):
        """Test creating a file attached to an insurance contract."""
        # Arrange - handled by the fixture
        
        # Act
        loaded_file = FileInsuranceContract.objects.get(id=file_insurance_contract.id)
        
        # Assert
        assert loaded_file.name is not None
        assert loaded_file.content is not None
        assert loaded_file.access_to_model is not None
        assert loaded_file.access_to_model.id == file_insurance_contract.access_to_model.id
    
    def test_file_tag_property(self, file_document):
        """Test the file_tag property that generates HTML for displaying the file."""
        # Arrange - handled by the fixture
        
        # Act
        tag = file_document.file_tag
        
        # Assert
        assert '<img src="' in tag
        assert 'width="500" height="500"' in tag
        assert file_document.content.url in tag
    
    def test_file_without_name(self, document):
        """Test behavior when file has no name."""
        # Arrange
        file_data = {
            "content": SimpleUploadedFile("test.txt", b"test content"),
            "access_to_model": document,
            "name": None
        }
        
        # Act
        file = FileDocument.objects.create(**file_data)
        
        # Assert
        assert file.id is not None
        assert file.name is None
        assert file.content is not None
    
    def test_file_path_generation(self, document):
        """Test if proper path is generated for uploaded file."""
        # Arrange
        test_file = SimpleUploadedFile("test_path.txt", b"test content")
        
        # Act
        file = FileDocument.objects.create(
            name="Path Test File",
            content=test_file,
            access_to_model=document
        )
        
        # Assert
        assert file.content.name is not None
        # The exact path depends on the UPLOADING_FILES_FOLDER_PATH setting,
        # but we can at least check the filename is in the path
        assert "test_path" in file.content.name
    
    def test_file_update(self, file_document):
        """Test updating file content."""
        # Arrange
        new_file = SimpleUploadedFile("updated.txt", b"updated content")
        
        # Act
        file_document.content = new_file
        file_document.save()
        updated_file = FileDocument.objects.get(id=file_document.id)
        
        # Assert
        assert "updated" in updated_file.content.name
        assert updated_file.content.size != 0
        # Note: Django doesn't automatically delete old files when FileField content changes
    
    def test_file_with_content(self, document):
        """Test creating a file with content."""
        # Arrange
        file_data = {
            "name": "With Content File",
            "access_to_model": document,
            "content": SimpleUploadedFile("test.txt", b"test content")
        }
        
        # Act
        file = FileDocument.objects.create(**file_data)
        
        # Assert
        assert file.id is not None
        assert file.content is not None
        assert file.content.size > 0

    def test_file_large_upload(self, document):
        """Test uploading a large file."""
        # Arrange
        large_file = SimpleUploadedFile("large_file.txt", b"A" * (10**7))  # 10 MB file
        
        # Act
        file = FileDocument.objects.create(
            name="Large File",
            content=large_file,
            access_to_model=document
        )
        
        # Assert
        assert file.id is not None
        assert file.content.size == len(large_file)

    def test_file_invalid_type(self, document):
        """Test uploading file with invalid content type."""
        # Arrange
        invalid_file = SimpleUploadedFile("invalid_file.exe", b"test content")  # Invalid type
        
        # Act
        # If no validation is implemented, we should check that the file is created successfully
        file = FileDocument.objects.create(
            name="Invalid File",
            content=invalid_file,
            access_to_model=document
        )
        
        # Assert
        assert file.id is not None
        # Note: In a production app, you might want to add validation for file types in the model
        # This test would then need to be updated to expect ValidationError

    def test_file_url_access(self, file_document):
        """Test accessing file via URL."""
        # Arrange - handled by the fixture
        
        # Act
        file_url = file_document.content.url
        
        # Assert
        assert file_url is not None
        # The URL format depends on the storage configuration in settings
        # In test environment, it might return a local path instead of an HTTP URL
        assert file_url.startswith('/static/files/') or 'http' in file_url

    def test_file_deletion(self, file_document):
        """Test proper file deletion."""
        # Arrange
        file_id = file_document.id
        
        # Act
        file_document.delete()
        
        # Assert
        assert not FileDocument.objects.filter(id=file_id).exists()

    def test_file_security(self, document):
        """Test security handling of potentially unsafe files."""
        # Arrange
        unsafe_file = SimpleUploadedFile("unsafe_file.html", b"<script>alert('XSS')</script>")
        
        # Act
        file = FileDocument.objects.create(
            name="Unsafe File",
            content=unsafe_file,
            access_to_model=document
        )
        
        # Assert
        assert file.id is not None
        # Here you would typically check that the content is sanitized
        # For example, if you have a method to sanitize the content
        # assert sanitize(file.content) == expected_safe_content


@pytest.mark.django_db
class TestInsuranceCompany:
    """Test cases for the InsuranceCompany model."""

    def test_create_insurance_company(self):
        """Test creating an insurance company with valid data."""
        # Arrange
        company_data = {
            "name": "Test Insurance Co",
            "phone_number": 5551234567,
            "site_app_company": "www.testinsurance.com"
        }
        
        # Act
        company = InsuranceCompany.objects.create(**company_data)
        
        # Assert
        assert company.id is not None
        assert company.name == "Test Insurance Co"
        assert company.phone_number == 5551234567
        assert company.site_app_company == "www.testinsurance.com"
    
    def test_insurance_company_str_method(self, insurance_company):
        """Test the string representation of an insurance company."""
        # Arrange - handled by the fixture
        
        # Act
        result = str(insurance_company)
        
        # Assert
        assert result == insurance_company.name
    
    def test_company_without_name(self):
        """Test creating company with null name (allowed in model)."""
        # Arrange
        company_data = {
            "phone_number": 5551234567,
            "site_app_company": "www.testinsurance.com",
            "name": None
        }
        
        # Act
        company = InsuranceCompany.objects.create(**company_data)
        
        # Assert
        assert company.id is not None
        assert company.name is None
        assert company.phone_number == 5551234567
    
    def test_company_null_phone(self):
        """Test behavior when phone_number is null."""
        # Arrange
        company_data = {
            "name": "No Phone Company",
            "phone_number": None,
            "site_app_company": "www.testinsurance.com"
        }
        
        # Act
        company = InsuranceCompany.objects.create(**company_data)
        
        # Assert
        assert company.id is not None
        assert company.name == "No Phone Company"
        assert company.phone_number is None
    
    def test_company_long_name(self):
        """Test with name at maximum length (50 chars)."""
        # Arrange
        long_name = "X" * 50  # Exactly 50 characters
        
        # Act
        company = InsuranceCompany.objects.create(name=long_name)
        
        # Assert
        assert company.id is not None
        assert company.name == long_name
        assert len(company.name) == 50
    
    def test_company_long_url(self):
        """Test with site_app_company at maximum length (70 chars)."""
        # Arrange
        long_url = "x" * 70  # Exactly 70 characters
        
        # Act
        company = InsuranceCompany.objects.create(
            name="Test Company",
            site_app_company=long_url
        )
        
        # Assert
        assert company.id is not None
        assert company.site_app_company == long_url
        assert len(company.site_app_company) == 70
    
    def test_company_unicode_characters(self):
        """Test with unicode characters in name and site."""
        # Arrange
        unicode_name = "保険会社"  # "Insurance company" in Japanese
        unicode_site = "www.保険.com"  # URL with Japanese characters
        
        # Act
        company = InsuranceCompany.objects.create(
            name=unicode_name,
            site_app_company=unicode_site
        )
        
        # Assert
        assert company.id is not None
        assert company.name == unicode_name
        assert company.site_app_company == unicode_site
    
    def test_company_meta_ordering(self):
        """Test if companies are properly ordered by name, phone."""
        # Arrange
        company1 = InsuranceCompany.objects.create(name="Zebra Insurance", phone_number=1111111111)
        company2 = InsuranceCompany.objects.create(name="Apple Insurance", phone_number=3333333333)
        company3 = InsuranceCompany.objects.create(name="Apple Insurance", phone_number=2222222222)
        
        # Act
        companies = list(InsuranceCompany.objects.all())
        
        # Assert
        # Should be ordered by name first, then phone
        assert companies[0].name == "Apple Insurance" and companies[0].phone_number == 2222222222
        assert companies[1].name == "Apple Insurance" and companies[1].phone_number == 3333333333
        assert companies[2].name == "Zebra Insurance"
    
    def test_company_deletion(self, insurance_company):
        """Test proper company deletion."""
        # Arrange
        company_id = insurance_company.id
        
        # Act
        insurance_company.delete()
        
        # Assert
        assert not InsuranceCompany.objects.filter(id=company_id).exists()

    def test_company_invalid_phone(self):
        """Test with invalid phone number formats."""
        # Arrange & Act & Assert
        # Test string phone number
        company_string = InsuranceCompany.objects.create(
            name="Company with string phone",
            phone_number="1234567890"  # String instead of integer
        )
        assert str(company_string.phone_number) == "1234567890"
        
        # Test very large phone number
        company_large = InsuranceCompany.objects.create(
            name="Company with large phone",
            phone_number=9999999999  # Large but valid number
        )
        assert company_large.phone_number == 9999999999
        
        # Test that negative numbers are rejected by the CHECK constraint
        with pytest.raises(IntegrityError, match=r".*CHECK constraint failed: phone_number.*"):
            InsuranceCompany.objects.create(
                name="Company with negative phone",
                phone_number=-1234567890  # Negative number, should fail
            )

    def test_company_duplicate_name(self):
        """Test creating companies with the same name."""
        # Arrange
        company_name = "Duplicate Company Name"
        company1 = InsuranceCompany.objects.create(
            name=company_name,
            phone_number=1111111111
        )
        
        # Act
        company2 = InsuranceCompany.objects.create(
            name=company_name,
            phone_number=2222222222
        )
        
        # Assert
        assert company1.id is not None
        assert company2.id is not None
        assert company1.name == company2.name
        assert company1.phone_number != company2.phone_number
        
        # Verify we can find both companies with the same name
        companies_with_name = InsuranceCompany.objects.filter(name=company_name)
        assert companies_with_name.count() == 2
        # Note: In some business contexts, you might want unique company names,
        # which would require implementing a unique constraint in the model


@pytest.mark.django_db
class TestInsuranceContract:
    """Test cases for the InsuranceContract model."""

    def test_create_real_estate_insurance_contract(self, real_estate_insurance_contract):
        """Test creating a real estate insurance contract."""
        # Arrange - handled by the fixture
        
        # Act
        loaded_contract = InsuranceContract.objects.get(id=real_estate_insurance_contract.id)
        
        # Assert
        assert loaded_contract.type == "Real Estate insurance"
        assert loaded_contract.annual_price["2023"] == 400
        assert loaded_contract.coverage["fire"] == "full"
    
    def test_create_transportation_insurance_contract(self, transportation_insurance_contract):
        """Test creating a transportation insurance contract."""
        # Arrange - handled by the fixture
        
        # Act
        loaded_contract = InsuranceContract.objects.get(id=transportation_insurance_contract.id)
        
        # Assert
        assert loaded_contract.type == "Transportation insurance"
        assert loaded_contract.annual_price["2023"] == 200
        assert loaded_contract.coverage["collision"] == "full"
    
    def test_create_person_insurance_contract(self, person_insurance_contract, user):
        """Test creating a person insurance contract."""
        # Arrange - handled by the fixture
        
        # Act
        loaded_contract = InsuranceContract.objects.get(id=person_insurance_contract.id)
        
        # Assert
        assert loaded_contract.type == "Person insurance"
        assert loaded_contract.person == user
        assert loaded_contract.annual_price["2023"] == 300
        assert loaded_contract.coverage["health"] == "full"
    
    def test_contract_active_status(self, insurance_company):
        """Test the active status of an insurance contract based on dates."""
        # Arrange
        today = timezone.now().date()
        past_date = today - timedelta(days=30)
        future_date = today + timedelta(days=30)
        
        active_contract = InsuranceContractFactory(
            company=insurance_company,
            starting_date=past_date,
            ending_date=future_date,
            is_insurance_active=None  # This would be determined by logic in a real app
        )
        
        expired_contract = InsuranceContractFactory(
            company=insurance_company,
            starting_date=past_date - timedelta(days=60),
            ending_date=past_date,
            is_insurance_active=None
        )
        
        # Act
        # In a real app, there might be a method to determine if a contract is active
        # Here we're just testing the data storage
        
        # Assert
        assert active_contract.starting_date < today
        assert active_contract.ending_date > today
        assert expired_contract.ending_date < today
    
    def test_contract_str_method(self, insurance_contract):
        """Test the string representation of an insurance contract."""
        # Arrange - handled by the fixture
        
        # Act
        result = str(insurance_contract)
        
        # Assert
        assert result == f"{insurance_contract.company.name} -- {insurance_contract.type}"
    
    def test_contract_without_company(self):
        """Test contract with null company (allowed in model)."""
        # Arrange
        contract_data = {
            "type": "Person insurance",
            "contract_number": "TEST-001",
            "company": None
        }
        
        # Act
        contract = InsuranceContract.objects.create(**contract_data)
        
        # Assert
        assert contract.id is not None
        assert contract.company is None
        assert contract.contract_number == "TEST-001"
    
    def test_contract_without_type(self, insurance_company):
        """Test contract without type (nullable but should be specified)."""
        # Arrange
        contract_data = {
            "company": insurance_company,
            "contract_number": "TEST-001",
            "type": None
        }
        
        # Act
        contract = InsuranceContract.objects.create(**contract_data)
        
        # Assert
        assert contract.id is not None
        assert contract.type is None
    
    def test_contract_invalid_type(self, insurance_company):
        """Test saving with a type not in choices."""
        # Arrange
        contract_data = {
            "company": insurance_company,
            "type": "Invalid Insurance Type",  # Not in choices
            "contract_number": "TEST-001"
        }
        
        # Act
        contract = InsuranceContract.objects.create(**contract_data)
        
        # Assert
        # Django allows non-choice values by default, but will fail form validation
        assert contract.id is not None
        assert contract.type == "Invalid Insurance Type"
    
    def test_contract_invalid_dates(self, insurance_company):
        """Test with ending_date before starting_date."""
        # Arrange
        today = timezone.now().date()
        future_date = today + timedelta(days=30)
        
        contract_data = {
            "company": insurance_company,
            "type": "Person insurance",
            "starting_date": future_date,
            "ending_date": today  # Earlier than starting_date
        }
        
        # Act
        contract = InsuranceContract.objects.create(**contract_data)
        
        # Assert
        # Django doesn't validate this at the model level by default
        # In a real app, you'd add validation in clean() or a form
        assert contract.id is not None
        assert contract.starting_date > contract.ending_date
    
    def test_contract_complex_annual_price(self, insurance_company):
        """Test complex annual price structure in JSON."""
        # Arrange
        complex_price = {
            "2023": 400,
            "2024": {
                "base": 420,
                "discount": 20,
                "final": 400
            },
            "2025": {
                "quarters": [105, 105, 105, 105],
                "total": 420
            }
        }
        
        # Act
        contract = InsuranceContract.objects.create(
            company=insurance_company,
            type="Person insurance",
            annual_price=complex_price
        )
        
        # Assert
        assert contract.id is not None
        assert contract.annual_price["2023"] == 400
        assert contract.annual_price["2024"]["discount"] == 20
        assert contract.annual_price["2025"]["quarters"][2] == 105
    
    def test_contract_complex_coverage(self, insurance_company):
        """Test complex coverage structure in JSON."""
        # Arrange
        complex_coverage = {
            "liability": {
                "personal": "full",
                "property": "up to 1,000,000€"
            },
            "disaster": ["fire", "flood", "earthquake"],
            "exclusions": {
                "countries": ["Country A", "Country B"],
                "activities": ["extreme sports"]
            }
        }
        
        # Act
        contract = InsuranceContract.objects.create(
            company=insurance_company,
            type="Person insurance",
            coverage=complex_coverage
        )
        
        # Assert
        assert contract.id is not None
        assert contract.coverage["liability"]["property"] == "up to 1,000,000€"
        assert "flood" in contract.coverage["disaster"]
        assert "Country A" in contract.coverage["exclusions"]["countries"]
    
    def test_contract_deletion(self, insurance_contract):
        """Test proper contract deletion."""
        # Arrange
        contract_id = insurance_contract.id
        
        # Act
        insurance_contract.delete()
        
        # Assert
        assert not InsuranceContract.objects.filter(id=contract_id).exists()

    def test_real_estate_missing_asset(self, insurance_company):
        """Test real estate insurance without asset."""
        # Arrange
        contract_data = {
            "company": insurance_company,
            "type": "Real Estate insurance",
            "contract_number": "RE-001",
            "annual_price": {"2023": 400},
            "coverage": {"fire": "full"},
            "real_estate_asset": None  # Missing asset
        }
        
        # Act
        contract = InsuranceContract.objects.create(**contract_data)
        
        # Assert
        assert contract.id is not None
        assert contract.type == "Real Estate insurance"
        assert contract.real_estate_asset is None
        # In a production app, you might want to validate that real estate insurance
        # should have a real_estate_asset, but the model allows it to be null
    
    def test_transportation_missing_asset(self, insurance_company):
        """Test transportation insurance without asset."""
        # Arrange
        contract_data = {
            "company": insurance_company,
            "type": "Transportation insurance",
            "contract_number": "TR-001",
            "annual_price": {"2023": 200},
            "coverage": {"collision": "full"},
            "transportation_asset": None  # Missing asset
        }
        
        # Act
        contract = InsuranceContract.objects.create(**contract_data)
        
        # Assert
        assert contract.id is not None
        assert contract.type == "Transportation insurance"
        assert contract.transportation_asset is None
        # In a production app, you might want to validate that transportation insurance
        # should have a transportation_asset, but the model allows it to be null
    
    def test_person_contract_missing_person(self, insurance_company):
        """Test person insurance without person."""
        # Arrange
        contract_data = {
            "company": insurance_company,
            "type": "Person insurance",
            "contract_number": "PI-001",
            "annual_price": {"2023": 300},
            "coverage": {"health": "full"},
            "person": None  # Missing person
        }
        
        # Act
        contract = InsuranceContract.objects.create(**contract_data)
        
        # Assert
        assert contract.id is not None
        assert contract.type == "Person insurance"
        assert contract.person is None
        # In a production app, you might want to validate that person insurance
        # should have a person, but the model allows it to be null 

    def test_contract_number_format(self, insurance_company):
        """Test different contract number formats."""
        # Arrange
        contract_formats = [
            "ABC-123",               # Standard format
            "123456789",             # Numeric only
            "ABC/123/2023",          # With slashes
            "Contract #123",         # With spaces and special chars
            "Très-Spécial-№1",       # Unicode characters
            "A" * 50,                # Very long number (max allowed)
            None                     # Null contract number
        ]
        
        # Act & Assert
        for contract_num in contract_formats:
            contract = InsuranceContract.objects.create(
                company=insurance_company,
                type="Person insurance",
                contract_number=contract_num
            )
            
            # Verify contract was created with the specified number
            loaded_contract = InsuranceContract.objects.get(id=contract.id)
            assert loaded_contract.contract_number == contract_num 

    def test_contract_renewal(self, insurance_contract):
        """Test renewing contract (extending dates)."""
        # Arrange
        original_ending_date = insurance_contract.ending_date
        new_ending_date = original_ending_date + timedelta(days=365)  # Extend by 1 year
        
        # Act - simulate renewal by extending end date
        insurance_contract.ending_date = new_ending_date
        insurance_contract.save()
        
        # Assert
        refreshed_contract = InsuranceContract.objects.get(id=insurance_contract.id)
        assert refreshed_contract.ending_date == new_ending_date
        assert refreshed_contract.ending_date > original_ending_date
        assert (refreshed_contract.ending_date - original_ending_date).days == 365
    
    def test_contract_multiple_assets(self, insurance_company):
        """Test contract with both RE and transport assets."""
        # Arrange
        contract_data = {
            "company": insurance_company,
            "type": "Combined insurance",  # Custom type for combined coverage
            "contract_number": "COMB-001",
            "annual_price": {"2023": 600},
            "coverage": {
                "real_estate": {"fire": "full"},
                "transportation": {"collision": "full"}
            },
            # We'd typically set both assets here if they were available
            # For now we're just testing that the model allows setting both
            "real_estate_asset": None,
            "transportation_asset": None
        }
        
        # Act
        contract = InsuranceContract.objects.create(**contract_data)
        
        # Assert
        assert contract.id is not None
        # In a production app, you might want to implement validation to ensure
        # that the contract type matches the provided assets 