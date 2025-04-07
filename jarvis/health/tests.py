from django.test import TestCase

# Create your tests here.

"""
Import tests from test directory.
"""
from .tests.test_api import (
    HealthAPITestCase,
    ProductAPITests,
    SymptomAPITests,
    BillAPITests
)
