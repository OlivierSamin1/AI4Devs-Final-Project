from django.db import models
from django.contrib.auth.models import User


class TaxManagementCompany(models.Model):
    """
    Tax management company model
    """
    name = models.CharField(max_length=50, blank=False, null=True)
    personal_email_used = models.EmailField(null=True, blank=True)
    site_app_company = models.CharField(max_length=70, blank=True, null=True, help_text="ex: myfoncia.com")
    comments = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        ordering = ['name', 'site_app_company', 'personal_email_used']
        verbose_name_plural = "Tax Management Companies"

    def __str__(self):
        return self.name


class TaxManagementContract(models.Model):
    """
    Tax management contract model
    """
    company = models.ForeignKey('tax.TaxManagementCompany', related_name='company', on_delete=models.CASCADE, blank=True, null=True)
    contract_number = models.CharField(max_length=50, blank=True, null=True)
    starting_date = models.DateField(blank=True, null=True)
    ending_date = models.DateField(blank=True, null=True)
    is_contract_active = models.BooleanField(null=True, blank=True)
    annual_price = models.JSONField(null=True, blank=True, help_text="ex: {'2020': 400, '2021': 400, ...}")

    class Meta:
        ordering = ['is_contract_active', 'company']
        verbose_name_plural = "Tax Management Contracts"

    def __str__(self):
        return self.company.name
