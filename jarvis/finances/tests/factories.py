"""
Factory classes for creating test instances of finances models.
"""
import factory
import json
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory
from datetime import date, timedelta

from finances.models import (
    Bank, 
    BankAccount,
    BankCard,
    BankAccountReport,
    FileAccount,
    FileCard,
    FileAccountReport
)
from finances.models.files import File

User = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    
    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'password')


class BankFactory(DjangoModelFactory):
    class Meta:
        model = Bank
    
    name = factory.Sequence(lambda n: f'Bank {n}')
    address = factory.Faker('address')
    postal_code = factory.Faker('random_int', min=10000, max=99999)
    country = factory.Faker('country')


class BankAccountFactory(DjangoModelFactory):
    class Meta:
        model = BankAccount
    
    bank = factory.SubFactory(BankFactory)
    titular = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: f'Account {n}')
    IBAN = factory.Sequence(lambda n: f'FR7630006000011234567890{n}')
    BIC = factory.Sequence(lambda n: f'BNPAFRPP{n}')
    starting_date = factory.LazyFunction(lambda: date.today() - timedelta(days=365))
    ending_date = factory.LazyFunction(lambda: date.today() + timedelta(days=365))
    is_account_open = True
    value_on_31_12 = factory.LazyFunction(lambda: {"2022": 10000.0, "2023": 12000.0})


class BankCardFactory(DjangoModelFactory):
    class Meta:
        model = BankCard
    
    bank_account = factory.SubFactory(BankAccountFactory)
    name = factory.Sequence(lambda n: f'Card {n}')
    is_active = True
    card_number = factory.Sequence(lambda n: f'4974123456789{n:03d}')
    ending_date = factory.LazyFunction(lambda: date.today() + timedelta(days=730))
    CCV = factory.Faker('random_int', min=100, max=999)


class BankAccountReportFactory(DjangoModelFactory):
    class Meta:
        model = BankAccountReport
    
    bank_account = factory.SubFactory(BankAccountFactory)
    date = factory.LazyFunction(lambda: date.today())


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


class FileAccountFactory(FileFactory):
    class Meta:
        model = FileAccount
    
    access_to_model = factory.SubFactory(BankAccountFactory)


class FileCardFactory(FileFactory):
    class Meta:
        model = FileCard
    
    access_to_model = factory.SubFactory(BankCardFactory)


class FileAccountReportFactory(FileFactory):
    class Meta:
        model = FileAccountReport
    
    access_to_model = factory.SubFactory(BankAccountReportFactory)
