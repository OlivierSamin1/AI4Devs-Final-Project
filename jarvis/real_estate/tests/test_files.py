"""
Tests for the File models in the real_estate app.
"""
import pytest
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile

from real_estate.models import (
    File, 
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


@pytest.mark.django_db
class TestBaseFile:
    """Test cases for the base File model."""

    def test_file_html_img_property(self, test_image):
        """Test the HTML image tag property of a file."""
        # Create a base file with an image
        file = File.objects.create(
            name="Test Image",
            content=test_image
        )
        
        # Check if the img_html property returns HTML with correct file name
        assert file.img_html is not None
        assert '<img src="' in file.img_html
        assert file.content.name in file.img_html


@pytest.mark.django_db
class TestFileAsset:
    """Test cases for the FileAsset model."""

    def test_create_file_asset(self, file_asset):
        """Test creating a file asset."""
        # Assert that the file asset was created correctly
        assert isinstance(file_asset, FileAsset)
        assert file_asset.id is not None
        assert file_asset.name is not None
        assert file_asset.access_to_model is not None
        
        # Check inheritance from base File model
        assert isinstance(file_asset, File)
        
    def test_file_asset_str_representation(self, file_asset):
        """Test the string representation of a file asset."""
        expected = f"{file_asset.name} - {file_asset.access_to_model}"
        assert str(file_asset) == expected


@pytest.mark.django_db
class TestFileBill:
    """Test cases for the FileBill model."""

    def test_create_file_bill(self, file_bill):
        """Test creating a file bill."""
        # Assert that the file bill was created correctly
        assert isinstance(file_bill, FileBill)
        assert file_bill.id is not None
        assert file_bill.name is not None
        assert file_bill.access_to_model is not None
        
        # Check inheritance from base File model
        assert isinstance(file_bill, File)
        
    def test_file_bill_str_representation(self, file_bill):
        """Test the string representation of a file bill."""
        expected = f"{file_bill.name} - {file_bill.access_to_model}"
        assert str(file_bill) == expected


@pytest.mark.django_db
class TestFileMortgage:
    """Test cases for the FileMortgage model."""

    def test_create_file_mortgage(self, file_mortgage):
        """Test creating a file mortgage."""
        # Assert that the file mortgage was created correctly
        assert isinstance(file_mortgage, FileMortgage)
        assert file_mortgage.id is not None
        assert file_mortgage.name is not None
        assert file_mortgage.access_to_model is not None
        
        # Check inheritance from base File model
        assert isinstance(file_mortgage, File)
        
    def test_file_mortgage_str_representation(self, file_mortgage):
        """Test the string representation of a file mortgage."""
        expected = f"{file_mortgage.name} - {file_mortgage.access_to_model}"
        assert str(file_mortgage) == expected


@pytest.mark.django_db
class TestFileTenant:
    """Test cases for the FileTenant model."""

    def test_create_file_tenant(self, file_tenant):
        """Test creating a file tenant."""
        # Assert that the file tenant was created correctly
        assert isinstance(file_tenant, FileTenant)
        assert file_tenant.id is not None
        assert file_tenant.name is not None
        assert file_tenant.access_to_model is not None
        
        # Check inheritance from base File model
        assert isinstance(file_tenant, File)
        
    def test_file_tenant_str_representation(self, file_tenant):
        """Test the string representation of a file tenant."""
        expected = f"{file_tenant.name} - {file_tenant.access_to_model}"
        assert str(file_tenant) == expected


@pytest.mark.django_db
class TestFileCoPro:
    """Test cases for the FileCoPro model."""

    def test_create_file_copro(self, file_copro):
        """Test creating a file copro."""
        # Assert that the file copro was created correctly
        assert isinstance(file_copro, FileCoPro)
        assert file_copro.id is not None
        assert file_copro.name is not None
        assert file_copro.access_to_model is not None
        
        # Check inheritance from base File model
        assert isinstance(file_copro, File)
        
    def test_file_copro_str_representation(self, file_copro):
        """Test the string representation of a file copro."""
        expected = f"{file_copro.name} - {file_copro.access_to_model}"
        assert str(file_copro) == expected


@pytest.mark.django_db
class TestFileRenting:
    """Test cases for the FileRenting model."""

    def test_create_file_renting(self, file_renting):
        """Test creating a file renting."""
        # Assert that the file renting was created correctly
        assert isinstance(file_renting, FileRenting)
        assert file_renting.id is not None
        assert file_renting.name is not None
        assert file_renting.access_to_model is not None
        
        # Check inheritance from base File model
        assert isinstance(file_renting, File)
        
    def test_file_renting_str_representation(self, file_renting):
        """Test the string representation of a file renting."""
        expected = f"{file_renting.name} - {file_renting.access_to_model}"
        assert str(file_renting) == expected


@pytest.mark.django_db
class TestFileUtility:
    """Test cases for the FileUtility model."""

    def test_create_file_utility(self, file_utility):
        """Test creating a file utility."""
        # Assert that the file utility was created correctly
        assert isinstance(file_utility, FileUtility)
        assert file_utility.id is not None
        assert file_utility.name is not None
        assert file_utility.access_to_model is not None
        
        # Check inheritance from base File model
        assert isinstance(file_utility, File)
        
    def test_file_utility_str_representation(self, file_utility):
        """Test the string representation of a file utility."""
        expected = f"{file_utility.name} - {file_utility.access_to_model}"
        assert str(file_utility) == expected


@pytest.mark.django_db
class TestFileHollyDaysPlatform:
    """Test cases for the FileHollyDaysPlatform model."""

    def test_create_file_holidays_platform(self, file_holidays_platform):
        """Test creating a file holidays platform."""
        # Assert that the file holidays platform was created correctly
        assert isinstance(file_holidays_platform, FileHollyDaysPlatform)
        assert file_holidays_platform.id is not None
        assert file_holidays_platform.name is not None
        assert file_holidays_platform.access_to_model is not None
        
        # Check inheritance from base File model
        assert isinstance(file_holidays_platform, File)
        
    def test_file_holidays_platform_str_representation(self, file_holidays_platform):
        """Test the string representation of a file holidays platform."""
        expected = f"{file_holidays_platform.name} - {file_holidays_platform.access_to_model}"
        assert str(file_holidays_platform) == expected


@pytest.mark.django_db
class TestFileHollyDaysReservation:
    """Test cases for the FileHollyDaysReservation model."""

    def test_create_file_holidays_reservation(self, file_holidays_reservation):
        """Test creating a file holidays reservation."""
        # Assert that the file holidays reservation was created correctly
        assert isinstance(file_holidays_reservation, FileHollyDaysReservation)
        assert file_holidays_reservation.id is not None
        assert file_holidays_reservation.name is not None
        assert file_holidays_reservation.access_to_model is not None
        
        # Check inheritance from base File model
        assert isinstance(file_holidays_reservation, File)
        
    def test_file_holidays_reservation_str_representation(self, file_holidays_reservation):
        """Test the string representation of a file holidays reservation."""
        expected = f"{file_holidays_reservation.name} - {file_holidays_reservation.access_to_model}"
        assert str(file_holidays_reservation) == expected


@pytest.mark.django_db
class TestFileUpload:
    """Test cases for file uploads across different file models."""
    
    def test_image_upload(self, asset, test_image):
        """Test uploading an image to a file asset."""
        # Create a file asset with an image
        file_asset = FileAsset.objects.create(
            name="Test Image Asset",
            content=test_image,
            access_to_model=asset
        )
        
        # Verify image content was saved
        assert file_asset.content is not None
        assert file_asset.content.name is not None
        
        # Check if content type was preserved
        if hasattr(file_asset.content, 'content_type'):
            assert 'image' in file_asset.content.content_type
    
    def test_document_upload(self, bill, test_document):
        """Test uploading a document to a file bill."""
        # Create a file bill with a document
        file_bill = FileBill.objects.create(
            name="Test Document Bill",
            content=test_document,
            access_to_model=bill
        )
        
        # Verify document content was saved
        assert file_bill.content is not None
        assert file_bill.content.name is not None
        
        # Check if content type was preserved
        if hasattr(file_bill.content, 'content_type'):
            assert 'pdf' in file_bill.content.content_type 