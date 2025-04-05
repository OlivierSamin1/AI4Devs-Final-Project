from django.db import models
from django.contrib.auth.models import User


class BankAccount(models.Model):
    bank = models.ForeignKey('finances.Bank', related_name='account', blank=False, null=True, on_delete=models.CASCADE)
    titular = models.ForeignKey(User, related_name='bank_account', blank=False, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=40, blank=False, null=True)
    IBAN = models.CharField(max_length=40, blank=False, null=True)
    BIC = models.CharField(max_length=20, blank=True, null=True)
    starting_date = models.DateField(blank=True, null=True)
    ending_date = models.DateField(blank=True, null=True)
    closing_account_date = models.DateField(blank=True, null=True)
    is_account_open = models.BooleanField(null=True, blank=False, default=True)
    value_on_31_12 = models.JSONField(null=True, blank=True, help_text="ex: {'2020': 1234.65, '2021': 2367.8}")

    class Meta:
        ordering = ['bank__name', 'is_account_open', 'IBAN']
        verbose_name_plural = "Bank Accounts"

    def __str__(self):
        return self.bank.name + " - " + self.name
