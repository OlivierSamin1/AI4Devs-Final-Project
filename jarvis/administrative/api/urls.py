"""
URL configuration for Administrative API.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from administrative.api.views import (
    DocumentViewSet,
    FileViewSet,
    InsuranceCompanyViewSet,
    InsuranceContractViewSet,
)

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'documents', DocumentViewSet, basename='document')
router.register(r'files', FileViewSet, basename='file')
router.register(r'insurance-companies', InsuranceCompanyViewSet, basename='insurance-company')
router.register(r'insurance-contracts', InsuranceContractViewSet, basename='insurance-contract')

# URL patterns for the API
urlpatterns = [
    # Include the router generated URLs
    path('', include(router.urls)),
    
    # Custom nested URLs for document files
    path('documents/<int:document_id>/files/', 
         DocumentViewSet.as_view({'get': 'files', 'post': 'upload_file'}), 
         name='document-files'),
    
    # Custom nested URLs for contract files
    path('insurance-contracts/<int:contract_id>/files/', 
         InsuranceContractViewSet.as_view({'get': 'files', 'post': 'upload_file'}), 
         name='contract-files'),
] 