from django.db import models


class Bank(models.Model):
    name = models.CharField(max_length=50, blank=False, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    postal_code = models.PositiveIntegerField(blank=True, null=True)
    country = models.CharField(max_length=200, help_text="69 RUE DU PORT", blank=True, null=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Banks"
        managed = False  # Important: don't try to manage this table
        
    def __str__(self):
        return self.name
