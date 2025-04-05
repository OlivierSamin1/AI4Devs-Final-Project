"""
File handling utilities for working with files across the application.
"""
import os
import io
import zipfile
import logging
import tempfile
import shutil
from django.http import FileResponse, HttpResponse
from jarvis import settings

logger = logging.getLogger(__name__)


def create_zip_file(files_list, zip_name="files.zip"):
    """
    Create a zip file from a list of file paths.
    
    Args:
        files_list: List of file paths or tuples (file_path, file_name_in_zip)
        zip_name: Name of the resulting zip file
    
    Returns:
        BytesIO object containing the zip file
    """
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for file_item in files_list:
            if isinstance(file_item, tuple):
                file_path, file_name = file_item
            else:
                file_path = file_item
                file_name = os.path.basename(file_path)
                
            try:
                zip_file.write(file_path, file_name)
            except Exception as e:
                logger.error(f"Error adding file {file_path} to zip: {str(e)}")
                
    return zip_buffer


def save_zip_file(zip_buffer, zip_path):
    """
    Save a BytesIO zip buffer to a file.
    
    Args:
        zip_buffer: BytesIO object containing the zip file
        zip_path: Path where the zip file should be saved
    """
    try:
        with open(zip_path, 'wb') as f:
            f.write(zip_buffer.getvalue())
        return True
    except Exception as e:
        logger.error(f"Error saving zip file to {zip_path}: {str(e)}")
        return False


def create_download_response(zip_buffer, filename):
    """
    Create an HTTP response for downloading a zip file.
    
    Args:
        zip_buffer: BytesIO object containing the zip file
        filename: Name of the file as it will appear when downloaded
    
    Returns:
        HttpResponse object configured for zip file download
    """
    response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


def get_static_file_path(relative_path):
    """
    Get the absolute path to a file in the static directory.
    
    Args:
        relative_path: Path relative to the static directory
    
    Returns:
        Absolute path to the file
    """
    return os.path.join(os.path.abspath(settings.BASE_DIR), 
                        "static", relative_path) 