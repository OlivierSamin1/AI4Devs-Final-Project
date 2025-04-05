"""
Factory classes for creating test instances of tax models.
"""
import factory
import random
import json
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory
from datetime import date, timedelta

from tax.models import (
    Tax, 
    TaxManagementCompany,
    TaxManagementContract,
    FileTax,
    FileTaxManagement
)
from tax.models.files import File

User = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    
    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'password')


class TaxManagementCompanyFactory(DjangoModelFactory):
    class Meta:
        model = TaxManagementCompany
    
    name = factory.Sequence(lambda n: f'Tax Company {n}')
    personal_email_used = factory.Faker('email')
    site_app_company = factory.Faker('domain_name')
    comments = factory.Faker('text', max_nb_chars=200)


class TaxManagementContractFactory(DjangoModelFactory):
    class Meta:
        model = TaxManagementContract
    
    company = factory.SubFactory(TaxManagementCompanyFactory)
    contract_number = factory.Sequence(lambda n: f'TC-{n:05d}')
    starting_date = factory.LazyFunction(lambda: date.today() - timedelta(days=365))
    ending_date = factory.LazyFunction(lambda: date.today() + timedelta(days=365))
    is_contract_active = factory.Faker('boolean', chance_of_getting_true=80)
    annual_price = factory.LazyFunction(
        lambda: {
            str(date.today().year - 1): 400,
            str(date.today().year): 425
        }
    )


class TaxFactory(DjangoModelFactory):
    class Meta:
        model = Tax
    
    name = factory.Sequence(lambda n: f'Tax {n}')
    tax_type = factory.LazyFunction(lambda: random.choice(['Real Estate tax', 'Transportation tax', 'Person tax', 'Other tax']))
    year = factory.LazyFunction(lambda: date.today().year)
    is_tax_management_company_used = factory.Faker('boolean', chance_of_getting_true=30)
    yearly_price = factory.Faker('pyfloat', left_digits=4, right_digits=2, positive=True, min_value=100, max_value=5000)
    personal_email_used = factory.Faker('email')
    site_app = factory.Faker('domain_name')
    
    @factory.post_generation
    def set_specific_tax_fields(self, create, extracted, **kwargs):
        if not create:
            return
        
        # Set fields based on tax_type
        if self.tax_type == 'Real Estate tax':
            self.real_estate_tax_type = random.choice(['IVI', 'Dustbin', 'Other'])
            # real_estate_asset would need to be set separately
        elif self.tax_type == 'Person tax':
            # person would need to be set separately
            pass
        elif self.tax_type == 'Transportation tax':
            # transportation_asset would need to be set separately
            pass
        
        if self.is_tax_management_company_used:
            self.tax_management_company = TaxManagementCompanyFactory()


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


class FileTaxFactory(FileFactory):
    class Meta:
        model = FileTax
    
    access_to_model = factory.SubFactory(TaxFactory)


class FileTaxManagementFactory(FileFactory):
    class Meta:
        model = FileTaxManagement
    
    access_to_model = factory.SubFactory(TaxManagementContractFactory) 