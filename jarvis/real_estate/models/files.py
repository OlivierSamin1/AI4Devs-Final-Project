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


class FileAsset(File):
    access_to_model = models.ForeignKey('real_estate.Asset', on_delete=models.CASCADE, null=True, blank=True, related_name='RE_asset_files')


class FileHollyDaysPlatform(File):
    access_to_model = models.ForeignKey('real_estate.HollydaysPlatform', on_delete=models.CASCADE, null=True, blank=True, related_name='RE_hollydays_platform_files')


class FileHollyDaysReservation(File):
    access_to_model = models.ForeignKey('real_estate.HollydaysReservation', on_delete=models.CASCADE, null=True, blank=True, related_name='RE_hollydays_reservation_files')


class FileBill(File):
    access_to_model = models.ForeignKey('real_estate.Bill', on_delete=models.CASCADE, null=True, blank=True, related_name='RE_bill_files')


class FileCoPro(File):
    access_to_model = models.ForeignKey('real_estate.CoProManagementContract', on_delete=models.CASCADE, null=True, blank=True, related_name='RE_copro_files')


class FileMortgage(File):
    access_to_model = models.ForeignKey('real_estate.Mortgage', on_delete=models.CASCADE, null=True, blank=True, related_name='RE_mortgage_files')


class FileRenting(File):
    access_to_model = models.ForeignKey('real_estate.RentingManagementContract', on_delete=models.CASCADE, null=True, blank=True, related_name='RE_renting_files')


class FileTenant(File):
    access_to_model = models.ForeignKey('real_estate.Tenant', on_delete=models.CASCADE, null=True, blank=True, related_name='RE_tenant_files')


class FileUtility(File):
    access_to_model = models.ForeignKey('real_estate.UtilityContract', on_delete=models.CASCADE, null=True, blank=True, related_name='RE_utility_files')
