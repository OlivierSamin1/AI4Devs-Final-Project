"""
Factory classes for creating test instances of administrative models.
"""
import factory
import json
import os
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory

from administrative.models import (
    Document, 
    File, 
    FileDocument,
    FileInsuranceContract,
    InsuranceCompany,
    InsuranceContract
)

User = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    
    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'password')


class DocumentFactory(DjangoModelFactory):
    class Meta:
        model = Document
    
    user = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: f'Document {n}')
    type = 'ID card'
    comment = factory.LazyFunction(lambda: {"expiry": "2025-01-01"})


class InsuranceCompanyFactory(DjangoModelFactory):
    class Meta:
        model = InsuranceCompany
    
    name = factory.Sequence(lambda n: f'Insurance Company {n}')
    phone_number = factory.Sequence(lambda n: int(f'12345{n}'))
    site_app_company = factory.LazyAttribute(lambda obj: f'www.{obj.name.lower().replace(" ", "")}.com')


class InsuranceContractFactory(DjangoModelFactory):
    class Meta:
        model = InsuranceContract
    
    company = factory.SubFactory(InsuranceCompanyFactory)
    type = 'Real Estate insurance'
    contract_number = factory.Sequence(lambda n: f'CONTRACT-{n}')
    starting_date = factory.Faker('date_object')
    ending_date = factory.Faker('date_object')
    is_insurance_active = True
    personal_email_used = factory.Faker('email')
    annual_price = factory.LazyFunction(lambda: {"2023": 400, "2024": 450})
    coverage = factory.LazyFunction(lambda: {"damage": "full", "theft": "partial"})


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


class FileDocumentFactory(FileFactory):
    class Meta:
        model = FileDocument
    
    access_to_model = factory.SubFactory(DocumentFactory)


class FileInsuranceContractFactory(FileFactory):
    class Meta:
        model = FileInsuranceContract
    
    access_to_model = factory.SubFactory(InsuranceContractFactory) 