"""
Insurance Company views for Administrative API.
"""

from rest_framework import viewsets, permissions
from django_filters import rest_framework as filters
from administrative.models import InsuranceCompany
from administrative.api.serializers.insurance_company_serializers import InsuranceCompanySerializer


class InsuranceCompanyFilter(filters.FilterSet):
    """Filter for InsuranceCompany queryset."""
    
    name = filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = InsuranceCompany
        fields = ['name', 'phone_number']


class InsuranceCompanyViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the InsuranceCompany model.
    
    This viewset provides `list`, `create`, `retrieve`, `update`, and `destroy` actions.
    """
    
    queryset = InsuranceCompany.objects.all()
    serializer_class = InsuranceCompanySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = InsuranceCompanyFilter 