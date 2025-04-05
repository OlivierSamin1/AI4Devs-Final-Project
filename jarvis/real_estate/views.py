from django.http import FileResponse
import os
from jarvis import settings
from dotenv import load_dotenv

load_dotenv()


def download_bills(request, zip_file_name):
    # Set the correct path to the directory where the zip files are stored
    zip_file_path = os.path.join('static/files', zip_file_name)

    # Create a FileResponse with the zip file's content
    response = FileResponse(open(zip_file_path, 'rb'), content_type='application/zip')

    # Set the Content-Disposition header
    response['Content-Disposition'] = f'attachment; filename="{zip_file_name}"'

    return response


def renting_download_bills(request, zip_file_name):
    # Set the correct path to the directory where the zip files are stored
    zip_file_path = os.path.join('static/files', zip_file_name)

    # Create a FileResponse with the zip file's content
    response = FileResponse(open(zip_file_path, 'rb'), content_type='application/zip')

    # Set the Content-Disposition header
    response['Content-Disposition'] = f'attachment; filename="{zip_file_name}"'

    return response


def download_bills_csv_details(request, csv_file_name):
    # Set the correct path to the directory where the csv files are stored
    csv_file_path = os.path.join('static/files', csv_file_name)

    # Create a FileResponse with the csv file's content
    response = FileResponse(open(csv_file_path, 'rb'), content_type='text/csv')

    # Set the Content-Disposition header
    response['Content-Disposition'] = f'attachment; filename="{csv_file_name}"'

    return response
