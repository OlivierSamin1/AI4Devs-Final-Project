import os
from django.db import models
from django.utils.html import mark_safe
from dotenv import load_dotenv
load_dotenv()


class File(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    content = models.FileField(upload_to=os.environ.get('UPLOADING_FILES_FOLDER_PATH'))

    class Meta:
        verbose_name_plural = "Files"

    @property
    def file_tag(self):
        return mark_safe('<img src="%s" width="500" height="500" />' % self.content.url)




class FileDocument(File):
    access_to_model = models.ForeignKey('administrative.Document', on_delete=models.CASCADE, null=True, blank=True, related_name='document_files')

class FileInsuranceContract(File):
    access_to_model = models.ForeignKey('administrative.InsuranceContract', on_delete=models.CASCADE, null=True, blank=True, related_name='insurance_contract_files')

