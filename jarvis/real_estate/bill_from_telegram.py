import os
from django.core.files.base import ContentFile
from django.core.files import File as DjangoFile
from .models import Bill, FileBill, File  # Replace with your Django model
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

def create_django_bill_fields(data, asset, client, file_path):
    print('ON-GOING = from file store in shared volume create an instance in files of bill model')
    print("file_path = ", file_path)
    file_name = file_path[::-1][file_path[::-1].find('_file') + 1 : file_path[::-1].find('/')][::-1]
    print("file_name = ", file_name)
    with open(file_path, "rb") as f:
        file_instance = File()
        file_instance.name = file_name
        file_instance.content.save(file_name, ContentFile(f.read()))
        print('file instance = ', file_instance)
        file_instance.save()
    is_tax_deductible = data.get('is_tax_deductible')
    bill_name = data.get('bill_name')
    date_str = data.get('date')
    total_price = data.get('total_price')
    tax_price = data.get('tax_price')
    price_tax_free = data.get('price_tax_free')

    # Convert the date string to a datetime object
    date = datetime.strptime(date_str, '%Y-%m-%d').date()
    # Create a new instance of the Bill model
    bill = Bill(
        asset=asset,
        client_name=client,
        bill_name=bill_name,
        date=date,
        total_price=float(total_price),
        tax=float(tax_price),
        price_without_tax=float(price_tax_free)
    )

    # Save the bill instance to the database
    bill.save()
    file_bill_instance = FileBill(content=file_instance)
    file_bill_instance.save()
    bill.RE_bill_files.add(file_bill_instance)

if __name__ == "__main__":
    create_django_bill_fields()
