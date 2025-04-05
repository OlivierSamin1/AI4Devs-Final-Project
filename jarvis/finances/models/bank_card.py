from django.db import models


class BankCard(models.Model):
    bank_account = models.ForeignKey('finances.BankAccount', related_name='card', blank=False, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, null=True, blank=False)
    is_active = models.BooleanField(null=True, blank=False, default=True)
    card_number = models.CharField(max_length=16, null=True, blank=True)
    ending_date = models.DateField(blank=True, null=True)
    CCV = models.CharField(blank=True, null=True, max_length=5)

    class Meta:
        ordering = ['bank_account__bank__name', 'name', 'card_number', 'ending_date', 'CCV']
        verbose_name_plural = "Bank Cards"
        managed = False  # Important: don't try to manage this table
        
    def __str__(self):
        return self.bank_account.bank.name if not self.name else self.bank_account.bank.name + " - " + self.name
