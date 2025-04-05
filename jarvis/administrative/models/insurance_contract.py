from django.db import models
from django.contrib.auth.models import User


def get_types():
    return [('Real Estate insurance', 'Real Estate insurance'), ('Transportation insurance', 'Transportation insurance'), ('Person insurance', 'Person insurance')]


class InsuranceContract(models.Model):
    company = models.ForeignKey('administrative.InsuranceCompany', related_name='contract', blank=False, null=True, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, null=True, blank=False, choices=get_types())
    real_estate_asset = models.ForeignKey('real_estate.Asset', blank=True, null=True, related_name='insurance_contract', on_delete=models.CASCADE, help_text="Fill only if type = Real Estate insurance")
    transportation_asset = models.ForeignKey('transportation.Asset', blank=True, null=True, related_name='insurance_contract', on_delete=models.CASCADE, help_text="Fill only if type = Transportation insurance")
    person = models.ForeignKey(User, blank=True, null=True, related_name='insurance_contract', on_delete=models.CASCADE, help_text="Fill only if type = Person insurance")
    contract_number = models.CharField(max_length=50, blank=True, null=True)
    starting_date = models.DateField(blank=True, null=True)
    ending_date = models.DateField(blank=True, null=True)
    is_insurance_active = models.BooleanField(null=True, blank=True)
    personal_email_used = models.EmailField(null=True, blank=True)
    annual_price = models.JSONField(null=True, blank=True, help_text="ex: {'2020': 400, '2021': 400, ...}")
    coverage = models.JSONField(null=True, blank=True, help_text='{"bricolage": "3 heures", ...}')

    class Meta:
        ordering = ['company', 'type', 'annual_price']
        verbose_name_plural = "Insurances"
        managed = False  # Important: don't try to manage this table

    def __str__(self):
        return self.company.name + ' -- ' + self.type
