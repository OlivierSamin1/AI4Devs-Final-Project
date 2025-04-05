from django.db import models
from django.contrib.auth.models import User


class Asset(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='transportation_asset', blank=True, null=True)
    type = models.CharField(max_length=30, blank=False, null=True, help_text='ex: Car, bike, moto...')
    brand = models.CharField(max_length=30, blank=False, null=True)
    model = models.CharField(max_length=50, blank=True, null=True)
    registration_number = models.CharField(max_length=20, blank=False, null=True, help_text='ex: 6347LMP')
    buying_date = models.DateField(blank=True, null=True)
    buying_price = models.PositiveIntegerField(blank=True, null=True)
    has_been_bought_new = models.BooleanField(blank=True, null=True)
    has_on_going_credit = models.BooleanField(blank=True, null=True, default=False)
    has_on_going_leasing = models.BooleanField(blank=True, null=True, default=False)
    last_itv_date = models.DateField(blank=True, null=True)
    next_itv_date = models.DateField(blank=True, null=True)
    comments = models.JSONField(blank=True, null=True)
    

    class Meta:
        ordering = ['type', 'brand', 'model']
        verbose_name_plural = "Assets"
        app_label = 'transportation'
        managed = False  # Important: don't try to manage this table

    def __str__(self):
        return self.type + ' - ' + self.brand
