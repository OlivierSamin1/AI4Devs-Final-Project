from django.db import models
from django.contrib.auth.models import User
from dotenv import load_dotenv
load_dotenv()


class Symptom(models.Model):
    """
    Health product
    """
    name = models.CharField(max_length=200, blank=False, null=True)
    child = models.BooleanField(blank=False, null=True)
    adult = models.BooleanField(blank=False, null=True)
    products = models.ManyToManyField('health.Product', related_name='product')
    comments = models.JSONField(null=True, blank=True, help_text='ex: {"comment 1": "details", "comment 2": "details"}')

    class Meta:
        ordering = ['name', 'adult', 'child']
        verbose_name_plural = "Symptoms"

    def __str__(self):
        name = self.name
        if self.child:
            name += " - child"
        if self.adult:
            name += " - adult"
        return name
