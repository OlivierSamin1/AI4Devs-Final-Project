from django.db import models
from django.contrib.auth.models import User


class Asset(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='real_estate_asset', blank=True, null=True)
    nickname = models.CharField(max_length=50, blank=False, null=True, help_text="nickname you want to give to this asset")
    address = models.CharField(max_length=200, blank=True, null=True)
    postal_code = models.PositiveIntegerField(blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)
    bank_accounts = models.ManyToManyField('finances.BankAccount', related_name='asset', related_query_name='asset', blank=True)
    buying_date = models.DateField(blank=True, null=True)
    buying_price = models.PositiveIntegerField(blank=True, null=True)
    has_on_going_mortgage = models.BooleanField(blank=True, null=True)
    is_rented = models.BooleanField(blank=True, null=True)
    renting_contract = models.OneToOneField('real_estate.RentingManagementContract', related_name='asset_renting_contract', blank=True, null=True, on_delete=models.CASCADE)
    copro_contract = models.OneToOneField('real_estate.CoproManagementContract', related_name='asset_copro_contract', blank=True, null=True, on_delete=models.CASCADE)
    is_our_living_house = models.BooleanField(blank=True, null=True)
    tax_management = models.ForeignKey('tax.TaxManagementContract', on_delete=models.CASCADE, related_name='asset', blank=True, null=True, help_text='this asset taxes are managed by a company?')
    details = models.JSONField(blank=True, null=True, help_text="ex: {'notary_number': 112345, ...")
    results_by_year = models.JSONField(blank=True, null=True)

    class Meta:
        ordering = ['owner', 'nickname', 'buying_date']
        verbose_name_plural = "Assets"
        managed = False  # Important: don't try to manage this table

    def __str__(self):
        return self.nickname
