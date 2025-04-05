from django.db import models

# Import models from the models package to make them available through this module
from transportation.models.asset import Asset
from transportation.models.files import File

__all__ = ['Asset', 'File']

# Create your models here.
