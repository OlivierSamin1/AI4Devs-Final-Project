"""
Factory classes for creating test instances of real_estate models.
"""
import factory
import json
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory
from datetime import date, timedelta

from real_estate.models import (
    Asset,
    Bill,
    Mortgage,
    Tenant,
    CoproManagementCompany,
    CoproManagementContract,
    RentingManagementCompany,
    RentingManagementContract,
    UtilitySupplier,
    UtilityContract,
    HollydaysPlatform,
    HollydaysReservation,
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

User = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    
    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'password')


class AssetFactory(DjangoModelFactory):
    class Meta:
        model = Asset
    
    owner = factory.SubFactory(UserFactory)
    nickname = factory.Sequence(lambda n: f'Property {n}')
    address = factory.Faker('street_address')
    postal_code = factory.Faker('random_int', min=10000, max=99999)
    city = factory.Faker('city')
    country = factory.Faker('country')
    buying_date = factory.LazyFunction(lambda: date.today() - timedelta(days=365*2))
    buying_price = factory.Faker('random_int', min=100000, max=1000000)
    has_on_going_mortgage = factory.Faker('boolean')
    is_rented = factory.Faker('boolean')
    is_our_living_house = factory.Faker('boolean')
    details = factory.LazyFunction(
        lambda: {
            "notary_number": factory.Faker('random_int', min=10000, max=99999),
            "floor": factory.Faker('random_int', min=1, max=10),
            "area": factory.Faker('random_int', min=30, max=200),
            "rooms": factory.Faker('random_int', min=1, max=6)
        }
    )
    results_by_year = factory.LazyFunction(
        lambda: {
            "2022": {"income": 12000, "expenses": 5000, "profit": 7000},
            "2023": {"income": 12500, "expenses": 4800, "profit": 7700}
        }
    )


class MortgageFactory(DjangoModelFactory):
    class Meta:
        model = Mortgage
    
    asset = factory.SubFactory(AssetFactory, has_on_going_mortgage=True)
    name = factory.Sequence(lambda n: f'Mortgage {n}')
    starting_date = factory.LazyFunction(lambda: date.today() - timedelta(days=365*2))
    ending_date = factory.LazyFunction(lambda: date.today() + timedelta(days=365*15))
    rate_renegociations = factory.LazyFunction(
        lambda: {
            "2020": "2.1%",
            "2022": "1.8%"
        }
    )
    annual_interests = factory.LazyFunction(
        lambda: {
            "2020": 4500,
            "2021": 4300,
            "2022": 4100
        }
    )
    annual_capital_refund = factory.LazyFunction(
        lambda: {
            "2020": 6000,
            "2021": 6200,
            "2022": 6400
        }
    )
    capital_due_end_of_year = factory.LazyFunction(
        lambda: {
            "2020": 194000,
            "2021": 187800,
            "2022": 181400
        }
    )


class TenantFactory(DjangoModelFactory):
    class Meta:
        model = Tenant
    
    asset = factory.SubFactory(AssetFactory, is_rented=True)
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    phone_number = factory.Faker('random_int', min=600000000, max=699999999)
    email = factory.Faker('email')
    id_type = factory.LazyFunction(lambda: factory.random.choice(['passport', 'dni', 'driver license']))
    id_number = factory.Faker('bothify', text='??######')
    bank_account_IBAN = factory.Faker('bothify', text='ES## #### #### #### #### ####')
    bank_account_recipient = factory.LazyAttribute(lambda o: f"{o.first_name} {o.last_name}")
    rental_starting_date = factory.LazyFunction(lambda: date.today() - timedelta(days=180))
    rental_ending_date = factory.LazyFunction(lambda: date.today() + timedelta(days=365))
    deposit_amount = factory.Faker('random_int', min=500, max=2000)
    is_actual_tenant = factory.Faker('boolean', chance_of_getting_true=90)
    has_guarantee = factory.Faker('boolean')
    comments = factory.LazyFunction(
        lambda: {
            "contract_details": "Standard 1-year contract",
            "payment_history": "Always on time",
            "maintenance_requests": ["Fixed shower", "Painted walls"]
        }
    )


class BillFactory(DjangoModelFactory):
    class Meta:
        model = Bill
    
    asset = factory.SubFactory(AssetFactory)
    company_name = factory.Faker('company')
    client_name = factory.SubFactory(UserFactory)
    bill_name = factory.Sequence(lambda n: f'Bill {n}')
    bill_comment = factory.Faker('sentence')
    is_tax_deductible = factory.Faker('boolean')
    is_location_commission_bill = factory.Faker('boolean')
    date = factory.LazyFunction(lambda: date.today() - timedelta(days=30))
    total_price = factory.Faker('pyfloat', left_digits=3, right_digits=2, positive=True)
    tax = factory.LazyFunction(lambda: factory.LazyAttribute('total_price') * 0.21)
    price_without_tax = factory.LazyFunction(lambda: factory.LazyAttribute('total_price') * 0.79)


class CoproManagementCompanyFactory(DjangoModelFactory):
    class Meta:
        model = CoproManagementCompany
    
    name = factory.Sequence(lambda n: f'Copro Management {n}')
    personal_email_used = factory.Faker('email')
    site_app_company = factory.Faker('domain_name')
    comments = factory.Faker('text', max_nb_chars=200)


class CoproManagementContractFactory(DjangoModelFactory):
    class Meta:
        model = CoproManagementContract
    
    company = factory.SubFactory(CoproManagementCompanyFactory)
    contract_number = factory.Sequence(lambda n: f'CM-{n:05d}')
    asset = factory.SubFactory(AssetFactory)
    starting_date = factory.LazyFunction(lambda: date.today() - timedelta(days=365))
    ending_date = factory.LazyFunction(lambda: date.today() + timedelta(days=365))
    is_management_active = factory.Faker('boolean', chance_of_getting_true=90)
    monthly_price = factory.Faker('pyfloat', left_digits=2, right_digits=2, positive=True, min_value=50, max_value=150)
    year = factory.LazyFunction(lambda: date.today().year)
    annual_expenses = factory.LazyFunction(
        lambda: {
            str(date.today().year - 1): {
                "fixed": 1400,
                "refurbishment": 300,
                "other": 120,
                "payment_delay": 100
            },
            str(date.today().year): {
                "fixed": 1450,
                "refurbishment": 0,
                "other": 80,
                "payment_delay": 0
            }
        }
    )


class RentingManagementCompanyFactory(DjangoModelFactory):
    class Meta:
        model = RentingManagementCompany
    
    name = factory.Sequence(lambda n: f'Renting Management {n}')
    personal_email_used = factory.Faker('email')
    site_app_company = factory.Faker('domain_name')
    comments = factory.Faker('text', max_nb_chars=200)


class RentingManagementContractFactory(DjangoModelFactory):
    class Meta:
        model = RentingManagementContract
    
    company = factory.SubFactory(RentingManagementCompanyFactory)
    contract_number = factory.Sequence(lambda n: f'RM-{n:05d}')
    asset = factory.SubFactory(AssetFactory, is_rented=True)
    starting_date = factory.LazyFunction(lambda: date.today() - timedelta(days=365))
    ending_date = factory.LazyFunction(lambda: date.today() + timedelta(days=365))
    is_management_active = factory.Faker('boolean', chance_of_getting_true=90)
    annual_results = factory.LazyFunction(
        lambda: {
            str(date.today().year - 1): {
                "expenses": 1400,
                "income": 9000,
                "net": 7600
            },
            str(date.today().year): {
                "expenses": 1200,
                "income": 9500,
                "net": 8300
            }
        }
    )


class UtilitySupplierFactory(DjangoModelFactory):
    class Meta:
        model = UtilitySupplier
    
    name = factory.Sequence(lambda n: f'Utility Provider {n}')
    personal_email_used = factory.Faker('email')
    phone = factory.Faker('bothify', text='6########')
    comments = factory.Faker('text', max_nb_chars=200)


class UtilityContractFactory(DjangoModelFactory):
    class Meta:
        model = UtilityContract
    
    supplier = factory.SubFactory(UtilitySupplierFactory)
    user = factory.SubFactory(UserFactory)
    personal_email_used = factory.Faker('email')
    asset = factory.SubFactory(AssetFactory)
    service = factory.LazyFunction(lambda: factory.random.choice(['Electricity', 'Water', 'Internet', 'Alarm', 'waste management', 'Other']))
    contract_number = factory.Sequence(lambda n: f'UTL-{n:05d}')
    starting_date = factory.LazyFunction(lambda: date.today() - timedelta(days=365))
    ending_date = factory.LazyFunction(lambda: date.today() + timedelta(days=365))
    year = factory.LazyFunction(lambda: date.today().year)
    monthly_price = factory.Faker('pyfloat', left_digits=2, right_digits=2, positive=True, min_value=30, max_value=150)
    payment_1 = factory.LazyAttribute(lambda o: o.monthly_price)
    payment_2 = factory.LazyAttribute(lambda o: o.monthly_price)
    payment_3 = factory.LazyAttribute(lambda o: o.monthly_price)
    payment_4 = factory.LazyAttribute(lambda o: o.monthly_price)
    payment_5 = factory.LazyAttribute(lambda o: o.monthly_price)
    payment_6 = factory.LazyAttribute(lambda o: o.monthly_price)
    payment_7 = factory.LazyAttribute(lambda o: o.monthly_price)
    payment_8 = factory.LazyAttribute(lambda o: o.monthly_price)
    payment_9 = factory.LazyAttribute(lambda o: o.monthly_price)
    payment_10 = factory.LazyAttribute(lambda o: o.monthly_price)
    payment_11 = factory.LazyAttribute(lambda o: o.monthly_price)
    payment_12 = factory.LazyAttribute(lambda o: o.monthly_price)
    installation_price = factory.Faker('random_int', min=0, max=500)
    date_installation = factory.LazyFunction(lambda: date.today() - timedelta(days=365))
    is_active = factory.Faker('boolean', chance_of_getting_true=90)
    comments = factory.Faker('text', max_nb_chars=200)


class HollydaysPlatformFactory(DjangoModelFactory):
    class Meta:
        model = HollydaysPlatform
    
    name = factory.Sequence(lambda n: f'Holiday Platform {n}')
    personal_email_used = factory.Faker('email')
    site_app_company = factory.Faker('domain_name')
    comments = factory.Faker('text', max_nb_chars=200)


class HollydaysReservationFactory(DjangoModelFactory):
    class Meta:
        model = HollydaysReservation
    
    platform = factory.SubFactory(HollydaysPlatformFactory)
    asset = factory.SubFactory(AssetFactory)
    reservation_number = factory.Sequence(lambda n: f'RES-{n:05d}')
    entry_date = factory.LazyFunction(lambda: date.today() - timedelta(days=7))
    number_of_nights = factory.Faker('random_int', min=1, max=14)
    end_date = factory.LazyAttribute(lambda o: o.entry_date + timedelta(days=o.number_of_nights))
    renting_person_full_name = factory.Faker('name')
    renting_person_dni = factory.Faker('bothify', text='??######')
    renting_person_direction = factory.Faker('street_address')
    renting_person_postcode = factory.Faker('postcode')
    renting_person_city = factory.Faker('city')
    renting_person_region = factory.Faker('state')
    renting_person_country = factory.Faker('country')
    price = factory.Faker('pyfloat', left_digits=3, right_digits=2, positive=True, min_value=300, max_value=1500)
    received_bank = factory.Faker('boolean')
    cleaning = factory.Faker('pyfloat', left_digits=2, right_digits=2, positive=True, min_value=50, max_value=150)
    commission_platform = factory.Faker('pyfloat', left_digits=2, right_digits=2, positive=True, min_value=30, max_value=200)
    commission_other = factory.Faker('pyfloat', left_digits=2, right_digits=2, positive=True, min_value=0, max_value=100)
    comments = factory.Faker('text', max_nb_chars=200)


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


class FileAssetFactory(FileFactory):
    class Meta:
        model = FileAsset
    
    access_to_model = factory.SubFactory(AssetFactory)


class FileBillFactory(FileFactory):
    class Meta:
        model = FileBill
    
    access_to_model = factory.SubFactory(BillFactory)


class FileMortgageFactory(FileFactory):
    class Meta:
        model = FileMortgage
    
    access_to_model = factory.SubFactory(MortgageFactory)


class FileTenantFactory(FileFactory):
    class Meta:
        model = FileTenant
    
    access_to_model = factory.SubFactory(TenantFactory)


class FileCoProFactory(FileFactory):
    class Meta:
        model = FileCoPro
    
    access_to_model = factory.SubFactory(CoproManagementContractFactory)


class FileRentingFactory(FileFactory):
    class Meta:
        model = FileRenting
    
    access_to_model = factory.SubFactory(RentingManagementContractFactory)


class FileUtilityFactory(FileFactory):
    class Meta:
        model = FileUtility
    
    access_to_model = factory.SubFactory(UtilityContractFactory)


class FileHollyDaysPlatformFactory(FileFactory):
    class Meta:
        model = FileHollyDaysPlatform
    
    access_to_model = factory.SubFactory(HollydaysPlatformFactory)


class FileHollyDaysReservationFactory(FileFactory):
    class Meta:
        model = FileHollyDaysReservation
    
    access_to_model = factory.SubFactory(HollydaysReservationFactory) 