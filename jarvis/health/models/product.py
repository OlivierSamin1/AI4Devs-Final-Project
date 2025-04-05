from django.db import models
from django.contrib.auth.models import User
from dotenv import load_dotenv
load_dotenv()


class Product(models.Model):
    """
    Health product
    """
    name = models.CharField(max_length=200, blank=False, null=True)
    natural = models.BooleanField(blank=False, null=True)
    child_use = models.BooleanField(blank=False, null=True)
    adult_use = models.BooleanField(blank=False, null=True)
    min_age = models.CharField(max_length=200, blank=True, null=True)
    source_info = models.CharField(max_length=200, blank=True, null=True)
    date_info = models.DateField(blank=True, null=True)
    composition = models.CharField(max_length=200, blank=True, null=True)
    interests = models.CharField(max_length=200, blank=True, null=True)
    comments = models.JSONField(null=True, blank=True, help_text='ex: {"comment 1": "details", "comment 2": "details"}')

    class Meta:
        ordering = ['name', 'natural', 'child_use', 'min_age']
        verbose_name_plural = "Products"

    def __str__(self):
        name = self.name
        if self.natural:
            name += " - natural"
        if self.child_use:
            name += " - child"
        if self.adult_use:
            name += " - adult"
        return name
