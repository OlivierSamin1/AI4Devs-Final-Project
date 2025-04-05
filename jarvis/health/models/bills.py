from django.db import models
from django.contrib.auth.models import User
from dotenv import load_dotenv
load_dotenv()


class Bill(models.Model):
    """
    'Bill related to health insurance'
    """
    company_name = models.CharField(max_length=50, blank=True, null=True)
    client_name = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='health_bill', blank=True, null=True)
    bill_name = models.CharField(max_length=50, blank=False, null=True, help_text="Give a meaningfull name at this bill")
    date = models.DateField(blank=True, null=True)
    total_price = models.FloatField(null=True, blank=True, help_text="price including tax")
    is_paid = models.BooleanField(default=False, blank=True, null=True)
    is_asked_by_us = models.BooleanField(default=False, blank=True, null=True)

    class Meta:
        ordering = ['client_name', 'bill_name', 'date', 'total_price', 'is_paid', 'is_asked_by_us']
        verbose_name_plural = "Bills"
        managed = False  # Important: don't try to manage this table

    def __str__(self):
        if self.company_name and self.bill_name:
            return self.company_name + " - " + self.bill_name
        return ""
