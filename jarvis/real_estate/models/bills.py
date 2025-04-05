from django.db import models
from django.contrib.auth.models import User
from dotenv import load_dotenv
import real_estate.constants as constants

load_dotenv()


class Bill(models.Model):
    """
    'Bill related to renting asset'
    """
    asset = models.ForeignKey('real_estate.Asset', related_name='bill', blank=False, null=True, on_delete=models.CASCADE, default=2)
    company_name = models.CharField(max_length=50, blank=True, null=True)
    client_name = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='bill', blank=True, null=True, default=1)
    bill_name = models.CharField(max_length=50, blank=False, null=True, help_text="Give a meaningfull name at this bill")
    bill_comment = models.CharField(max_length=50, blank=True, null=True, help_text="Give a meaningfull description of this bill. It will be used for tax deduction")
    is_tax_deductible = models.BooleanField(null=True, blank=True, default=True)
    is_location_commission_bill = models.BooleanField(null=True, blank=True, default=False)
    date = models.DateField(blank=True, null=True)
    total_price = models.FloatField(null=True, blank=True, help_text="price including tax")
    tax = models.FloatField(null=True, blank=True, help_text="tax price")
    price_without_tax = models.FloatField(null=True, blank=True, help_text="price without tax")

    class Meta:
        ordering = ['asset', 'bill_name', 'date', 'total_price']
        verbose_name_plural = "Bills"
        managed = False  # Important: don't try to manage this table

    def auto_correct_bill_name(self):
        for key, value in constants.mapping_bill_name.items():
            if self.bill_name == key:
                self.bill_name = value

        for key, value in constants.containing_bill_name.items():
            if key in self.bill_name:
                self.bill_name = value

    def auto_comment_bill(self):
        for key, value in constants.mapping_bill_comment.items():
            if self.bill_name == key:
                self.bill_comment = value

    def save(self, *args, **kwargs):
        self.auto_correct_bill_name()
        self.auto_comment_bill()
        super().save(*args, **kwargs)

    def __str__(self):
        if self.company_name and self.bill_name and self.asset.nickname:
            return self.company_name + " - " + self.bill_name + ' - ' + self.asset.nickname
        return ""
