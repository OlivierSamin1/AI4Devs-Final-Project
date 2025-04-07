"""
Views for the Health app.
"""
from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Import the API views
from .api.views import (
    ProductViewSet, SymptomViewSet, BillViewSet,
    FileViewSet, FileBillViewSet, FileProductViewSet, FileSymptomViewSet
)

# Add any additional non-API views here
