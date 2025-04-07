"""
URL configuration for the Health API.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ProductViewSet, SymptomViewSet, BillViewSet,
    FileViewSet, FileBillViewSet, FileProductViewSet, FileSymptomViewSet
)

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'symptoms', SymptomViewSet, basename='symptom')
router.register(r'bills', BillViewSet, basename='bill')
router.register(r'files', FileViewSet, basename='file')
router.register(r'bill-files', FileBillViewSet, basename='bill-file')
router.register(r'product-files', FileProductViewSet, basename='product-file')
router.register(r'symptom-files', FileSymptomViewSet, basename='symptom-file')

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
] 