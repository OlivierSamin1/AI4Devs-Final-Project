"""
Tests for the health app models.
"""
import pytest
import json
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from datetime import date, timedelta
import uuid

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


@pytest.mark.django_db
class TestBill:
    
    def test_create_bill_with_valid_data(self, user):
        # Arrange & Act
        bill = BillFactory(
            company_name="Test Company",
            client_name=user,
            bill_name="Test Bill",
            date=date.today(),
            total_price=100.50,
            is_paid=True,
            is_asked_by_us=False
        )
        
        # Assert
        assert bill.company_name == "Test Company"
        assert bill.client_name == user
        assert bill.bill_name == "Test Bill"
        assert bill.date == date.today()
        assert bill.total_price == 100.50
        assert bill.is_paid is True
        assert bill.is_asked_by_us is False
    
    def test_bill_str_method(self, bill):
        # Arrange
        # bill fixture is already created
        
        # Act
        result = str(bill)
        
        # Assert
        assert result == f"{bill.company_name} - {bill.bill_name}"
    
    def test_bill_without_company(self, bill_without_company):
        # Arrange
        # bill_without_company fixture is already created
        
        # Act
        result = str(bill_without_company)
        
        # Assert
        assert result == ""
        assert bill_without_company.company_name is None
    
    def test_bill_without_client(self, bill_without_client):
        # Arrange
        # bill_without_client fixture is already created
        
        # Assert
        assert bill_without_client.client_name is None
    
    def test_bill_date_validation(self, user):
        # Arrange & Act
        past_date = date.today() - timedelta(days=30)
        future_date = date.today() + timedelta(days=30)
        
        past_bill = BillFactory(client_name=user, date=past_date)
        future_bill = BillFactory(client_name=user, date=future_date)
        
        # Assert
        assert past_bill.date == past_date
        assert future_bill.date == future_date
    
    def test_bill_paid_status(self, paid_bill, unpaid_bill):
        # Arrange
        # paid_bill and unpaid_bill fixtures are already created
        
        # Assert
        assert paid_bill.is_paid is True
        assert unpaid_bill.is_paid is False
    
    def test_bill_asked_by_us_status(self, asked_by_us_bill):
        # Arrange
        # asked_by_us_bill fixture is already created
        
        # Assert
        assert asked_by_us_bill.is_asked_by_us is True
    
    def test_bill_total_price(self, user):
        # Arrange & Act
        bill1 = BillFactory(client_name=user, total_price=100.00)
        bill2 = BillFactory(client_name=user, total_price=9999.99)
        
        # Assert
        assert bill1.total_price == 100.00
        assert bill2.total_price == 9999.99
    
    def test_bill_negative_price(self, user):
        # Arrange & Act
        bill = BillFactory(client_name=user, total_price=-50.00)
        
        # Assert
        assert bill.total_price == -50.00
    
    def test_bill_zero_price(self, user):
        # Arrange & Act
        bill = BillFactory(client_name=user, total_price=0.00)
        
        # Assert
        assert bill.total_price == 0.00
    
    def test_bill_long_company_name(self):
        # Arrange
        long_name = "C" * 50  # Maximum length is 50
        
        # Act
        bill = BillFactory(company_name=long_name)
        
        # Assert
        assert bill.company_name == long_name
        assert len(bill.company_name) == 50
    
    def test_bill_long_name(self):
        # Arrange
        long_name = "B" * 50  # Maximum length is 50
        
        # Act
        bill = BillFactory(bill_name=long_name)
        
        # Assert
        assert bill.bill_name == long_name
        assert len(bill.bill_name) == 50
    
    def test_bill_unicode_characters(self):
        # Arrange & Act
        bill = BillFactory(
            company_name="Compagnie Médicale",
            bill_name="Facture Générale"
        )
        
        # Assert
        assert bill.company_name == "Compagnie Médicale"
        assert bill.bill_name == "Facture Générale"
    
    def test_bill_deletion(self, bill):
        # Arrange
        bill_id = bill.id
        
        # Act
        bill.delete()
        
        # Assert
        assert Bill.objects.filter(id=bill_id).count() == 0
    
    def test_bill_with_files(self, bill):
        # Arrange
        file = FileBillFactory(access_to_model=bill)
        
        # Act
        files = FileBill.objects.filter(access_to_model=bill)
        
        # Assert
        assert files.count() == 1
        assert files.first().access_to_model == bill


@pytest.mark.django_db
class TestProduct:
    
    def test_create_product_with_valid_data(self):
        # Arrange & Act
        product = ProductFactory(
            name="Test Product",
            natural=True,
            child_use=True,
            adult_use=True,
            min_age="3",
            source_info="Test Source",
            date_info=date.today(),
            composition="Test Composition",
            interests="Test Interests",
            comments={"usage": "Test Usage"}
        )
        
        # Assert
        assert product.name == "Test Product"
        assert product.natural is True
        assert product.child_use is True
        assert product.adult_use is True
        assert product.min_age == "3"
        assert product.source_info == "Test Source"
        assert product.date_info == date.today()
        assert product.composition == "Test Composition"
        assert product.interests == "Test Interests"
        assert product.comments["usage"] == "Test Usage"
    
    def test_product_str_method(self, product):
        # Arrange
        # product fixture is already created
        expected_str = product.name
        if product.natural:
            expected_str += " - natural"
        if product.child_use:
            expected_str += " - child"
        if product.adult_use:
            expected_str += " - adult"
        
        # Act
        result = str(product)
        
        # Assert
        assert result == expected_str
    
    def test_product_without_name(self):
        # Arrange & Act
        product = ProductFactory(name=None)
        
        # Assert
        assert product.name is None
    
    def test_product_natural(self, natural_product):
        # Arrange
        # natural_product fixture is already created
        
        # Assert
        assert natural_product.natural is True
        assert " - natural" in str(natural_product)
    
    def test_product_child_use(self, child_product):
        # Arrange
        # child_product fixture is already created
        
        # Assert
        assert child_product.child_use is True
        assert child_product.adult_use is False
        assert " - child" in str(child_product)
    
    def test_product_adult_use(self, adult_product):
        # Arrange
        # adult_product fixture is already created
        
        # Assert
        assert adult_product.child_use is False
        assert adult_product.adult_use is True
        assert " - adult" in str(adult_product)
    
    def test_product_min_age(self):
        # Arrange & Act
        product = ProductFactory(min_age="12")
        
        # Assert
        assert product.min_age == "12"
    
    def test_product_source_info(self):
        # Arrange & Act
        product = ProductFactory(source_info="Scientific Journal Vol.5")
        
        # Assert
        assert product.source_info == "Scientific Journal Vol.5"
    
    def test_product_date_info(self):
        # Arrange
        test_date = date(2023, 5, 15)
        
        # Act
        product = ProductFactory(date_info=test_date)
        
        # Assert
        assert product.date_info == test_date
    
    def test_product_composition(self):
        # Arrange & Act
        product = ProductFactory(composition="Ingredient 1, Ingredient 2, Ingredient 3")
        
        # Assert
        assert product.composition == "Ingredient 1, Ingredient 2, Ingredient 3"
    
    def test_product_interests(self):
        # Arrange & Act
        product = ProductFactory(interests="Reduces inflammation, Boosts immunity")
        
        # Assert
        assert product.interests == "Reduces inflammation, Boosts immunity"
    
    def test_product_json_comments(self, product_with_comments):
        # Arrange
        product = product_with_comments
        
        # Assert
        assert product.comments["usage"] == "Take 2 tablets daily"
        assert product.comments["side_effects"] == "Nausea, headache, dizziness"
        assert product.comments["storage"] == "Keep below 25°C"
        assert "active_ingredient_1" in product.comments["ingredients"]
        assert product.comments["research"]["studies"] == 3
        assert product.comments["research"]["findings"] == "Effective in 85% of cases"
        assert len(product.comments["research"]["publication_dates"]) == 3
    
    def test_product_long_name(self):
        # Arrange
        long_name = "P" * 200  # Maximum length is 200
        
        # Act
        product = ProductFactory(name=long_name)
        
        # Assert
        assert product.name == long_name
        assert len(product.name) == 200
    
    def test_product_unicode_characters(self):
        # Arrange & Act
        product = ProductFactory(
            name="Remède Naturel",
            composition="Extraits de plantes, Huiles essentielles"
        )
        
        # Assert
        assert product.name == "Remède Naturel"
        assert product.composition == "Extraits de plantes, Huiles essentielles"
    
    def test_product_deletion(self, product):
        # Arrange
        product_id = product.id
        
        # Act
        product.delete()
        
        # Assert
        assert Product.objects.filter(id=product_id).count() == 0
    
    def test_product_with_files(self, product):
        # Arrange
        file = FileProductFactory(access_to_model=product)
        
        # Act
        files = FileProduct.objects.filter(access_to_model=product)
        
        # Assert
        assert files.count() == 1
        assert files.first().access_to_model == product


@pytest.mark.django_db
class TestSymptom:
    
    def test_create_symptom_with_valid_data(self):
        # Arrange & Act
        symptom = SymptomFactory(
            name="Test Symptom",
            child=True,
            adult=True,
            comments={"severity": "moderate"}
        )
        
        # Assert
        assert symptom.name == "Test Symptom"
        assert symptom.child is True
        assert symptom.adult is True
        assert symptom.comments["severity"] == "moderate"
    
    def test_symptom_str_method(self, symptom):
        # Arrange
        # symptom fixture is already created
        expected_str = symptom.name
        if symptom.child:
            expected_str += " - child"
        if symptom.adult:
            expected_str += " - adult"
        
        # Act
        result = str(symptom)
        
        # Assert
        assert result == expected_str
    
    def test_symptom_without_name(self):
        # Arrange & Act
        symptom = SymptomFactory(name=None)
        
        # Assert
        assert symptom.name is None
    
    def test_symptom_child(self, child_symptom):
        # Arrange
        # child_symptom fixture is already created
        
        # Assert
        assert child_symptom.child is True
        assert child_symptom.adult is False
        assert " - child" in str(child_symptom)
    
    def test_symptom_adult(self, adult_symptom):
        # Arrange
        # adult_symptom fixture is already created
        
        # Assert
        assert adult_symptom.child is False
        assert adult_symptom.adult is True
        assert " - adult" in str(adult_symptom)
    
    def test_symptom_both_age_flags(self):
        # Arrange & Act
        symptom = SymptomFactory(child=True, adult=True)
        
        # Assert
        assert symptom.child is True
        assert symptom.adult is True
        assert " - child" in str(symptom)
        assert " - adult" in str(symptom)
    
    def test_symptom_with_products(self, symptom_with_products):
        # Arrange
        # symptom_with_products fixture is already created
        
        # Act
        products = symptom_with_products.products.all()
        
        # Assert
        assert products.count() == 2
    
    def test_symptom_without_products(self, symptom):
        # Arrange
        # symptom fixture is already created
        
        # Act
        products = symptom.products.all()
        
        # Assert
        assert products.count() == 0
    
    def test_symptom_json_comments(self, symptom_with_comments):
        # Arrange
        symptom = symptom_with_comments
        
        # Assert
        assert "mild" in symptom.comments["severity"]
        assert "moderate" in symptom.comments["severity"]
        assert "severe" in symptom.comments["severity"]
        assert symptom.comments["duration"] == "1-2 weeks"
        assert "viral infection" in symptom.comments["common_causes"]
        assert symptom.comments["preventive_measures"] == "Hand washing, avoiding contact with sick people"
        assert "age" in symptom.comments["risk_factors"]
        assert "immunodeficiency" in symptom.comments["risk_factors"]["conditions"]
    
    def test_symptom_long_name(self):
        # Arrange
        long_name = "S" * 200  # Maximum length is 200
        
        # Act
        symptom = SymptomFactory(name=long_name)
        
        # Assert
        assert symptom.name == long_name
        assert len(symptom.name) == 200
    
    def test_symptom_unicode_characters(self):
        # Arrange & Act
        symptom = SymptomFactory(name="Maux de Tête")
        
        # Assert
        assert symptom.name == "Maux de Tête"
    
    def test_symptom_deletion(self, symptom):
        # Arrange
        symptom_id = symptom.id
        
        # Act
        symptom.delete()
        
        # Assert
        assert Symptom.objects.filter(id=symptom_id).count() == 0
    
    def test_symptom_with_files(self, symptom):
        # Arrange
        file = FileSymptomFactory(access_to_model=symptom)
        
        # Act
        files = FileSymptom.objects.filter(access_to_model=symptom)
        
        # Assert
        assert files.count() == 1
        assert files.first().access_to_model == symptom


@pytest.mark.django_db
class TestFile:
    
    def test_file_tag_property(self, file_bill):
        # Arrange
        # file_bill fixture is already created
        
        # Act
        tag = file_bill.file_tag
        
        # Assert
        assert '<img src=' in tag
        assert 'width="500" height="500"' in tag
    
    def test_file_without_name(self, bill):
        # Arrange & Act
        file = FileBillFactory(
            access_to_model=bill,
            name=None
        )
        
        # Assert
        assert file.name is None
    
    def test_file_with_content(self, bill, test_image):
        # Arrange & Act
        file = FileBillFactory(
            access_to_model=bill,
            content=test_image
        )
        
        # Assert
        assert file.content.name.endswith('.jpg')
        assert file.content.size > 0
    
    def test_file_bill_creation(self, bill):
        # Arrange & Act
        file = FileBillFactory(access_to_model=bill)
        
        # Assert
        assert file.access_to_model == bill
    
    def test_file_product_creation(self, product):
        # Arrange & Act
        file = FileProductFactory(access_to_model=product)
        
        # Assert
        assert file.access_to_model == product
    
    def test_file_symptom_creation(self, symptom):
        # Arrange & Act
        file = FileSymptomFactory(access_to_model=symptom)
        
        # Assert
        assert file.access_to_model == symptom
    
    def test_file_deletion(self, file_bill):
        # Arrange
        file_id = file_bill.id
        
        # Act
        file_bill.delete()
        
        # Assert
        assert not FileBill.objects.filter(id=file_id).exists()
    
    def test_file_relationships(self, bill, product, symptom):
        # Arrange
        file_bill = FileBillFactory(access_to_model=bill)
        file_product = FileProductFactory(access_to_model=product)
        file_symptom = FileSymptomFactory(access_to_model=symptom)
        
        # Act - Get related models
        bill_file_model = file_bill.access_to_model
        product_file_model = file_product.access_to_model
        symptom_file_model = file_symptom.access_to_model
        
        # Assert
        assert bill_file_model == bill
        assert product_file_model == product
        assert symptom_file_model == symptom
    
    def test_cross_model_file_reference(self, bill, product):
        # Arrange
        file_bill = FileBillFactory(access_to_model=bill)
        file_product = FileProductFactory(access_to_model=product)
        
        # Act & Assert
        assert file_bill.access_to_model._meta.model_name == 'bill'
        assert file_product.access_to_model._meta.model_name == 'product' 