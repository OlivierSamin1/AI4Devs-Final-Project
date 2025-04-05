from django.db import models
from django.contrib.auth.models import User


class RentingManagementCompany(models.Model):
    """
    Renting management company model
    """
    name = models.CharField(max_length=50, blank=False, null=True)
    personal_email_used = models.EmailField(null=True, blank=True)
    site_app_company = models.CharField(max_length=70, blank=True, null=True, help_text="ex: myfoncia.com")
    comments = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Renting Management Companies"
        managed = False  # Important: don't try to manage this table
    def __str__(self):
        return self.name


class RentingManagementContract(models.Model):
    """
    Renting management contract model
    """
    company = models.ForeignKey('real_estate.RentingManagementCompany', related_name='contract', blank=False, null=True, on_delete=models.CASCADE)
    contract_number = models.CharField(max_length=50, blank=True, null=True)
    asset = models.OneToOneField('real_estate.Asset', related_name='renting_contract_asset', on_delete=models.CASCADE, blank=True, null=True)
    starting_date = models.DateField(blank=True, null=True)
    ending_date = models.DateField(blank=True, null=True)
    is_management_active = models.BooleanField(null=True, blank=True)
    annual_results = models.JSONField(null=True, blank=True, help_text="ex: {'2020': {'expenses': 1400, 'income': 9000, 'net': 7600}}")

    class Meta:
        ordering = ['is_management_active', 'company__name', 'asset']
        verbose_name_plural = "Renting Managements"
        managed = False  # Important: don't try to manage this table

    def __str__(self):
        return str(self.company)
