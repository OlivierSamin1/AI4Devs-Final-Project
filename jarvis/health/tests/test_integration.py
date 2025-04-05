"""
Integration tests for the health app models.
These tests verify the interactions between different models.
"""
import pytest
from datetime import date, timedelta
from django.contrib.auth import get_user_model

from health.models import (
    Bill,
    Product, 
    Symptom,
    FileBill,
    FileProduct,
    FileSymptom
)
from health.models.files import File
from .factories import (
    BillFactory,
    ProductFactory,
    SymptomFactory,
    FileBillFactory,
    FileProductFactory,
    FileSymptomFactory
)

User = get_user_model()


@pytest.mark.django_db
class TestHealthIntegration:
    
    def test_user_with_multiple_bills(self, user):
        """Test user with multiple bills."""
        # Arrange
        bill1 = BillFactory(client_name=user, bill_name="Doctor Visit")
        bill2 = BillFactory(client_name=user, bill_name="Medication")
        bill3 = BillFactory(client_name=user, bill_name="Lab Tests")
        
        # Act
        user_bills = Bill.objects.filter(client_name=user)
        
        # Assert
        assert user_bills.count() == 3
        assert set(user_bills.values_list('bill_name', flat=True)) == {"Doctor Visit", "Medication", "Lab Tests"}
    
    def test_product_with_multiple_files(self, product):
        """Test product with multiple attached files."""
        # Arrange
        file1 = FileProductFactory(access_to_model=product, name="Product Image")
        file2 = FileProductFactory(access_to_model=product, name="Product Documentation")
        file3 = FileProductFactory(access_to_model=product, name="Research Paper")
        
        # Act
        files = FileProduct.objects.filter(access_to_model=product)
        
        # Assert
        assert files.count() == 3
        assert set(files.values_list('name', flat=True)) == {"Product Image", "Product Documentation", "Research Paper"}
    
    def test_symptom_with_multiple_files(self, symptom):
        """Test symptom with multiple attached files."""
        # Arrange
        file1 = FileSymptomFactory(access_to_model=symptom, name="Symptom Diagram")
        file2 = FileSymptomFactory(access_to_model=symptom, name="Medical Reference")
        
        # Act
        files = FileSymptom.objects.filter(access_to_model=symptom)
        
        # Assert
        assert files.count() == 2
        assert set(files.values_list('name', flat=True)) == {"Symptom Diagram", "Medical Reference"}
    
    def test_bill_with_multiple_files(self, bill):
        """Test bill with multiple attached files."""
        # Arrange
        file1 = FileBillFactory(access_to_model=bill, name="Receipt")
        file2 = FileBillFactory(access_to_model=bill, name="Insurance Claim")
        
        # Act
        files = FileBill.objects.filter(access_to_model=bill)
        
        # Assert
        assert files.count() == 2
        assert set(files.values_list('name', flat=True)) == {"Receipt", "Insurance Claim"}
    
    def test_symptom_with_multiple_products(self):
        """Test symptom associated with multiple products."""
        # Arrange
        product1 = ProductFactory(name="Medicine A")
        product2 = ProductFactory(name="Medicine B")
        product3 = ProductFactory(name="Medicine C")
        
        symptom = SymptomFactory(name="Headache")
        symptom.products.add(product1, product2, product3)
        
        # Act
        symptom_products = symptom.products.all()
        
        # Assert
        assert symptom_products.count() == 3
        assert set(symptom_products.values_list('name', flat=True)) == {"Medicine A", "Medicine B", "Medicine C"}
    
    def test_product_for_multiple_symptoms(self):
        """Test product used for multiple symptoms."""
        # Arrange
        product = ProductFactory(name="Pain Reliever")
        
        symptom1 = SymptomFactory(name="Headache")
        symptom2 = SymptomFactory(name="Joint Pain")
        symptom3 = SymptomFactory(name="Fever")
        
        symptom1.products.add(product)
        symptom2.products.add(product)
        symptom3.products.add(product)
        
        # Act
        product_symptoms = Symptom.objects.filter(products=product)
        
        # Assert
        assert product_symptoms.count() == 3
        assert set(product_symptoms.values_list('name', flat=True)) == {"Headache", "Joint Pain", "Fever"}
    
    def test_bill_cascade_delete(self, bill):
        """Test deleting bill cascades to files."""
        # Arrange
        file1 = FileBillFactory(access_to_model=bill)
        file2 = FileBillFactory(access_to_model=bill)
        
        file_ids = [file1.id, file2.id]
        
        # Act
        bill.delete()
        
        # Assert
        assert FileBill.objects.filter(id__in=file_ids).count() == 0
    
    def test_product_cascade_delete(self, product):
        """Test deleting product cascades to files."""
        # Arrange
        file1 = FileProductFactory(access_to_model=product)
        file2 = FileProductFactory(access_to_model=product)
        
        file_ids = [file1.id, file2.id]
        
        # Act
        product.delete()
        
        # Assert
        assert FileProduct.objects.filter(id__in=file_ids).count() == 0
    
    def test_symptom_cascade_delete(self, symptom):
        """Test deleting symptom cascades to files."""
        # Arrange
        file1 = FileSymptomFactory(access_to_model=symptom)
        file2 = FileSymptomFactory(access_to_model=symptom)
        
        file_ids = [file1.id, file2.id]
        
        # Act
        symptom.delete()
        
        # Assert
        assert FileSymptom.objects.filter(id__in=file_ids).count() == 0
    
    def test_user_health_overview(self, user):
        """Test retrieving all health data for a user."""
        # Arrange
        bill1 = BillFactory(client_name=user, company_name="Hospital A")
        bill2 = BillFactory(client_name=user, company_name="Pharmacy B")
        
        file1 = FileBillFactory(access_to_model=bill1)
        file2 = FileBillFactory(access_to_model=bill2)
        
        # Act
        user_bills = Bill.objects.filter(client_name=user)
        bill_ids = user_bills.values_list('id', flat=True)
        bill_files = FileBill.objects.filter(access_to_model__in=bill_ids)
        
        # Assert
        assert user_bills.count() == 2
        assert bill_files.count() == 2
        assert set(user_bills.values_list('company_name', flat=True)) == {"Hospital A", "Pharmacy B"}
    
    def test_product_age_compatibility(self):
        """Test product age compatibility with symptoms."""
        # Arrange
        child_product = ProductFactory(
            name="Children's Medicine",
            child_use=True,
            adult_use=False,
            min_age="2"
        )
        
        adult_product = ProductFactory(
            name="Adult Medicine",
            child_use=False,
            adult_use=True,
            min_age="18"
        )
        
        all_ages_product = ProductFactory(
            name="Family Medicine",
            child_use=True,
            adult_use=True,
            min_age="1"
        )
        
        child_symptom = SymptomFactory(name="Child Fever", child=True, adult=False)
        adult_symptom = SymptomFactory(name="Adult Migraine", child=False, adult=True)
        all_ages_symptom = SymptomFactory(name="Common Cold", child=True, adult=True)
        
        # Create appropriate relationships
        child_symptom.products.add(child_product, all_ages_product)
        adult_symptom.products.add(adult_product, all_ages_product)
        all_ages_symptom.products.add(child_product, adult_product, all_ages_product)
        
        # Act & Assert
        # Child symptom should have child-appropriate products
        child_products = child_symptom.products.filter(child_use=True)
        assert child_products.count() == 2
        
        # Adult symptom should have adult-appropriate products
        adult_products = adult_symptom.products.filter(adult_use=True)
        assert adult_products.count() == 2
        
        # Common symptoms should have products for all
        common_products = all_ages_symptom.products.all()
        assert common_products.count() == 3
    
    def test_complete_health_structure(self, user):
        """Test complete health data structure for a user."""
        # Arrange
        # Create bills
        bill1 = BillFactory(client_name=user, bill_name="Doctor Visit")
        bill2 = BillFactory(client_name=user, bill_name="Pharmacy Purchase")
        
        # Create products
        product1 = ProductFactory(name="Pain Reliever")
        product2 = ProductFactory(name="Antibiotic")
        
        # Create symptoms
        symptom1 = SymptomFactory(name="Headache")
        symptom2 = SymptomFactory(name="Infection")
        
        # Associate products with symptoms
        symptom1.products.add(product1)
        symptom2.products.add(product2)
        
        # Create files
        bill_file = FileBillFactory(access_to_model=bill1)
        product_file = FileProductFactory(access_to_model=product1)
        symptom_file = FileSymptomFactory(access_to_model=symptom1)
        
        # Act
        user_bills = Bill.objects.filter(client_name=user)
        all_products = Product.objects.all()
        all_symptoms = Symptom.objects.all()
        
        bill_files = FileBill.objects.filter(access_to_model__in=user_bills)
        product_files = FileProduct.objects.all()
        symptom_files = FileSymptom.objects.all()
        
        # Assert
        assert user_bills.count() == 2
        assert all_products.count() == 2
        assert all_symptoms.count() == 2
        
        assert bill_files.count() == 1
        assert product_files.count() == 1
        assert symptom_files.count() == 1
        
        assert symptom1.products.count() == 1
        assert symptom2.products.count() == 1
    
    def test_file_relationships_health(self, bill, product, symptom):
        """Test file relationships across health models."""
        # Arrange
        file_bill = FileBillFactory(access_to_model=bill)
        file_product = FileProductFactory(access_to_model=product)
        file_symptom = FileSymptomFactory(access_to_model=symptom)
        
        # Act - Get files through relationships
        bill_files = bill.health_bill_files.all()
        product_files = product.natural_product.all()
        symptom_files = symptom.natural_symptom.all()
        
        # Assert
        assert bill_files.count() == 1
        assert bill_files.first() == file_bill
        
        assert product_files.count() == 1
        assert product_files.first() == file_product
        
        assert symptom_files.count() == 1
        assert symptom_files.first() == file_symptom
    
    def test_cross_model_file_reference_health(self, bill, product, symptom):
        """Test file objects reference correct health model types."""
        # Arrange
        file_bill = FileBillFactory(access_to_model=bill)
        file_product = FileProductFactory(access_to_model=product)
        file_symptom = FileSymptomFactory(access_to_model=symptom)
        
        # Act & Assert
        assert file_bill.access_to_model._meta.model_name == 'bill'
        assert file_product.access_to_model._meta.model_name == 'product'
        assert file_symptom.access_to_model._meta.model_name == 'symptom' 