import os.path
import subprocess
from django.urls import reverse
from django.contrib import messages
import io
import zipfile
import logging
from django.http import HttpResponse
from jarvis import settings
from dotenv import load_dotenv
from core.utils.file_handling import create_zip_file, save_zip_file, create_download_response

load_dotenv()
logger = logging.getLogger(__name__)


class BillFiles:
    ZIP_FILE_NAME = "bills.zip"
    ZIP_PATH = os.path.join('static/files', ZIP_FILE_NAME)
    logger.info('zip path = {}'.format(ZIP_PATH))
    
    def handle(self, request, queryset):
        files_to_zip = []
        
        for bill_instance in queryset:
            files = bill_instance.RE_bill_files.all()
            for file in files:
                # Access the 'content' field directly from the 'file' instance
                file_path = file.content.path
                file_name = file.content.name.split('/')[-1]
                files_to_zip.append((file_path, file_name))
        
        # Create zip file using utility
        zip_buffer = create_zip_file(files_to_zip, self.ZIP_FILE_NAME)
        
        # Save the zip file to the path
        save_zip_file(zip_buffer, self.ZIP_PATH)
        
        # Create download response
        response = create_download_response(zip_buffer, self.ZIP_FILE_NAME)
        
        # Create a download link in the message
        download_url = reverse('bills_download', args=[self.ZIP_FILE_NAME])
        message = f'Download the bills zip file here: http://192.168.1.128:8000{download_url}'
        messages.add_message(request, messages.INFO, message)
        
        return response
