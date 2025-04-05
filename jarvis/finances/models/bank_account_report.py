from django.db import models


class BankAccountReport(models.Model):
    bank_account = models.ForeignKey('finances.BankAccount', related_name='bank_account', blank=False, null=True, on_delete=models.CASCADE)
    date = models.DateField(blank=False, null=True)

    class Meta:
        ordering = ['bank_account', 'date']
        verbose_name_plural = "Bank Account Reports"

    def set_date_to_str(self):
        return str(self.date.year) + str(self.date.month)

    def __str__(self):
        return str(self.bank_account) + " - " + self.set_date_to_str()
