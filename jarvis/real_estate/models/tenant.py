from django.db import models


class Tenant(models.Model):
    asset = models.OneToOneField('real_estate.Asset', related_name='tenant', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=False, null=True)
    last_name = models.CharField(max_length=50, blank=False, null=True)
    phone_number = models.PositiveIntegerField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    id_type = models.CharField(max_length=50, blank=False, null=True)
    id_number = models.CharField(max_length=50, blank=False, null=True)
    bank_account_IBAN = models.CharField(max_length=50, null=True, blank=True)
    bank_account_recipient = models.CharField(max_length=100, blank=True, null=True)
    rental_starting_date = models.DateField(blank=False, null=True)
    rental_ending_date = models.DateField(blank=True, null=True)
    deposit_amount = models.PositiveSmallIntegerField(blank=True, null=True)
    is_actual_tenant = models.BooleanField(blank=False, null=True)
    has_guarantee = models.BooleanField(null=True, blank=True, default=False)
    comments = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ['asset', 'is_actual_tenant', 'last_name', 'first_name']
        verbose_name_plural = "Tenants"

    def __str__(self):
        return self.first_name + ' ' + self.last_name
