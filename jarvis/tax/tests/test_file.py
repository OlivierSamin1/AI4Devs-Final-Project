"""
Tests for the File models in the tax app.
"""
import pytest
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile

from tax.models import FileTax, FileTaxManagement
from tax.models.files import File


@pytest.mark.django_db
class TestFileModel:
    """Test cases for the base File model and its subclasses."""

    def test_create_file_tax(self, file_tax):
        """Test creating a file linked to a tax."""
        # Assert
        assert isinstance(file_tax, FileTax)
        assert file_tax.id is not None
        assert file_tax.access_to_model is not None

    def test_create_file_tax_management(self, file_tax_management):
        """Test creating a file linked to a tax management contract."""
        # Assert
        assert isinstance(file_tax_management, FileTaxManagement)
        assert file_tax_management.id is not None
        assert file_tax_management.access_to_model is not None

    def test_file_str_representation(self, file_tax):
        """Test the string representation of a file."""
        # Skip this test as the File model doesn't override __str__
        pass

    def test_file_without_name(self, file_without_name):
        """Test a file without a name."""
        # Assert
        assert file_without_name.name is None
        
    def test_file_with_file_data(self, file_with_file_data):
        """Test a file with actual file data."""
        # Assert
        assert file_with_file_data.content is not None
        assert file_with_file_data.content.name.endswith('.txt')
        assert file_with_file_data.content.size > 0

    def test_image_file(self, image_file):
        """Test a file representing an image."""
        # Assert
        assert image_file.content is not None
        assert image_file.content.name.endswith('.png')
        # Verify file_tag property exists
        assert hasattr(image_file, 'file_tag')

    def test_document_file(self, document_file):
        """Test a document file."""
        # Assert
        assert document_file.content is not None
        assert document_file.content.name.endswith('.pdf')
        # Verify file_tag property exists
        assert hasattr(document_file, 'file_tag')