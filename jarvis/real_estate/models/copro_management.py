from django.db import models
from django.contrib.auth.models import User


class CoproManagementCompany(models.Model):
    """
    Copro management company model
    """
    name = models.CharField(max_length=50, blank=False, null=True)
    personal_email_used = models.EmailField(null=True, blank=True)
    site_app_company = models.CharField(max_length=70, blank=True, null=True, help_text="ex: myfoncia.com")
    comments = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Copro Management Companies"
        managed = False  # Important: don't try to manage this table

    def __str__(self):
        return self.name


class CoproManagementContract(models.Model):
    """
    Copro management contract model
    """
    company = models.OneToOneField('real_estate.CoproManagementCompany', related_name='copro_contract_company', blank=False, null=True, on_delete=models.CASCADE)
    contract_number = models.CharField(max_length=50, blank=True, null=True)
    asset = models.OneToOneField('real_estate.Asset', related_name='copro_contract_tenant', on_delete=models.CASCADE, null=True, blank=True)
    starting_date = models.DateField(blank=True, null=True)
    ending_date = models.DateField(blank=True, null=True)
    is_management_active = models.BooleanField(null=True, blank=True)
    monthly_price = models.FloatField(null=True, blank=True, default=0, help_text="If it is an annual price, divide it by twelve")
    year = models.SmallIntegerField(null=True, blank=True, default=2023)
    annual_expenses = models.JSONField(null=True, blank=True, help_text="ex: {'2020': {'fixed': 1400, 'refurbishment': 300, 'other': 12, 'payment_delay': 100}}")

    class Meta:
        ordering = ['company__name', 'is_management_active']
        verbose_name_plural = "Copro Management Contracts"
        managed = False  # Important: don't try to manage this table

    def __str__(self):
        return self.company.name
