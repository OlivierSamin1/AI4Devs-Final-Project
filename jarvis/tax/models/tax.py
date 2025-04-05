from django.db import models
from django.contrib.auth.models import User


def get_tax_choices():
    return [('Real Estate tax', 'Real Estate tax'), ('Transportation tax', 'Transportation tax'), ('Person tax', 'Person tax'), ('Other tax', 'Other tax')]

def get_real_estate_tax_choices():
    return [('IVI', 'IVI'), ('Dustbin', 'Dustbin'), ('Other', 'Other')]


class Tax(models.Model):
    """
    Tax model to get instances of habitation tax ...
    """
    name = models.CharField(max_length=100, blank=False, null=True)
    tax_type = models.CharField(max_length=50, null=True, blank=True, choices=get_tax_choices())

    real_estate_asset = models.ForeignKey('real_estate.Asset', blank=True, null=True, related_name='tax', on_delete=models.CASCADE, help_text="Fill only if type = Real Estate tax")
    real_estate_tax_type = models.CharField(max_length=50, null=True, blank=True, choices=get_real_estate_tax_choices())
    transportation_asset = models.ForeignKey('transportation.Asset', blank=True, null=True, related_name='tax', on_delete=models.CASCADE, help_text="Fill only if type = Transportation tax")
    year = models.PositiveSmallIntegerField(blank=True, null=True)
    person = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='tax', help_text="Fill only if type = Person tax")
    is_tax_management_company_used = models.BooleanField(null=True, blank=True, default=False)
    tax_management_company = models.ForeignKey('tax.TaxManagementCompany', blank=True, null=True, on_delete=models.CASCADE, related_name='tax', help_text='Fill only if is_tax_management_company_used is True')
    yearly_price = models.FloatField(null=True, blank=True, default=0)
    personal_email_used = models.EmailField(null=True, blank=True)
    site_app = models.CharField(max_length=70, blank=True, null=True, help_text="ex: impots.gouv.fr")

    class Meta:
        ordering = ['name', 'tax_type']
        verbose_name_plural = "Taxes"

    def __str__(self):
        return self.name
