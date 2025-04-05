from django.db import models
from django.contrib.auth.models import User


UTILITY_CHOICES = [("waste management", "waste management"), ("Electricity", "Electricity"), ("Water", "Water"), ("Internet", "Internet"), ("Alarm", "Alarm"), ("Other", "Other")]


class UtilitySupplier(models.Model):
    """
    Utility supplier model
    """
    name = models.CharField(max_length=50, blank=False, null=True)
    personal_email_used = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=12, blank=True, null=True, help_text="ex: 682882017")
    comments = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Utility suppliers"
        managed = False  # Important: don't try to manage this table
    def __str__(self):
        return self.name


class UtilityContract(models.Model):
    """
    Utility model
    """
    supplier = models.ForeignKey('real_estate.UtilitySupplier', related_name='utility_supplier', blank=False, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='utility', blank=False, null=True)
    personal_email_used = models.EmailField(null=True, blank=True)
    asset = models.ForeignKey('real_estate.Asset', related_name='utility_tenant', on_delete=models.CASCADE, blank=False, null=True)
    service = models.CharField(max_length=50, choices=UTILITY_CHOICES, blank=False, null=True)
    contract_number = models.CharField(max_length=50, blank=True, null=True)
    starting_date = models.DateField(blank=True, null=True)
    ending_date = models.DateField(blank=True, null=True)
    year = models.SmallIntegerField(null=True, blank=True, default=2023)
    monthly_price = models.FloatField(null=True, blank=True, default=0, help_text="If it is an annual price, divide it by twelve")
    payment_1 = models.FloatField(null=True, blank=True, default=0)
    payment_2 = models.FloatField(null=True, blank=True, default=0)
    payment_3 = models.FloatField(null=True, blank=True, default=0)
    payment_4 = models.FloatField(null=True, blank=True, default=0)
    payment_5 = models.FloatField(null=True, blank=True, default=0)
    payment_6 = models.FloatField(null=True, blank=True, default=0)
    payment_7 = models.FloatField(null=True, blank=True, default=0)
    payment_8 = models.FloatField(null=True, blank=True, default=0)
    payment_9 = models.FloatField(null=True, blank=True, default=0)
    payment_10 = models.FloatField(null=True, blank=True, default=0)
    payment_11 = models.FloatField(null=True, blank=True, default=0)
    payment_12 = models.FloatField(null=True, blank=True, default=0)
    installation_price = models.FloatField(null=True, blank=True, default=0)
    date_installation = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)


    class Meta:
        ordering = ['service', 'asset', 'user', 'is_active']
        verbose_name_plural = "Utility Contracts"

    def __str__(self):
        return self.service + " - " + str(self.asset) + " - " + str(self.user)
