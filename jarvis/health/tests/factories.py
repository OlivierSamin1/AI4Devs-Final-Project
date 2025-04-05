"""
Factory classes for creating test instances of health models.
"""
import factory
import json
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory
from datetime import date, timedelta

from health.models import (
    Bill,
    Product,
    Symptom,
    FileBill,
    FileProduct,
    FileSymptom
)
from health.models.files import File

User = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    
    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'password')


class BillFactory(DjangoModelFactory):
    class Meta:
        model = Bill
    
    company_name = factory.Sequence(lambda n: f'Company {n}')
    client_name = factory.SubFactory(UserFactory)
    bill_name = factory.Sequence(lambda n: f'Bill {n}')
    date = factory.LazyFunction(lambda: date.today())
    total_price = factory.Faker('pyfloat', left_digits=3, right_digits=2, positive=True)
    is_paid = factory.Faker('boolean')
    is_asked_by_us = factory.Faker('boolean')


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product
    
    name = factory.Sequence(lambda n: f'Product {n}')
    natural = factory.Faker('boolean')
    child_use = factory.Faker('boolean')
    adult_use = factory.Faker('boolean')
    min_age = factory.Sequence(lambda n: f'{n}')
    source_info = factory.Faker('sentence')
    date_info = factory.LazyFunction(lambda: date.today() - timedelta(days=30))
    composition = factory.Faker('sentence')
    interests = factory.Faker('sentence')
    comments = factory.LazyFunction(
        lambda: {
            "usage": "Take as directed by physician",
            "side_effects": "May cause drowsiness",
            "storage": "Store in a cool, dry place"
        }
    )


class SymptomFactory(DjangoModelFactory):
    class Meta:
        model = Symptom
    
    name = factory.Sequence(lambda n: f'Symptom {n}')
    child = factory.Faker('boolean')
    adult = factory.Faker('boolean')
    comments = factory.LazyFunction(
        lambda: {
            "severity": "mild to moderate",
            "duration": "typically 3-5 days",
            "common_causes": "viral infection, allergies"
        }
    )
    
    @factory.post_generation
    def products(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        
        for product in extracted:
            self.products.add(product)


class FileFactory(DjangoModelFactory):
    class Meta:
        model = File
        abstract = True
    
    name = factory.Sequence(lambda n: f'File {n}')
    content = factory.LazyFunction(
        lambda: SimpleUploadedFile(
            name='test_file.txt',
            content=b'This is a test file content',
            content_type='text/plain'
        )
    )


class FileBillFactory(FileFactory):
    class Meta:
        model = FileBill
    
    access_to_model = factory.SubFactory(BillFactory)


class FileProductFactory(FileFactory):
    class Meta:
        model = FileProduct
    
    access_to_model = factory.SubFactory(ProductFactory)


class FileSymptomFactory(FileFactory):
    class Meta:
        model = FileSymptom
    
    access_to_model = factory.SubFactory(SymptomFactory) 