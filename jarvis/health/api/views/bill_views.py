"""
Bill views for the Health API.
"""
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as filters

from health.models import Bill, FileBill
from ..serializers.bill_serializers import BillSerializer, BillDetailSerializer
from ..serializers.file_serializers import FileBillSerializer


class BillFilter(filters.FilterSet):
    """
    Filter for Bill queryset.
    """
    company_name = filters.CharFilter(lookup_expr='icontains')
    client_name = filters.NumberFilter(field_name='client_name__id')
    is_paid = filters.BooleanFilter()
    is_asked_by_us = filters.BooleanFilter()
    date_after = filters.DateFilter(field_name='date', lookup_expr='gte')
    date_before = filters.DateFilter(field_name='date', lookup_expr='lte')
    
    class Meta:
        model = Bill
        fields = [
            'company_name', 'client_name', 'is_paid', 
            'is_asked_by_us', 'date_after', 'date_before'
        ]


class BillViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Bills.
    """
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = BillFilter
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BillDetailSerializer
        return self.serializer_class
    
    @action(detail=True, methods=['get'])
    def files(self, request, pk=None):
        """
        Get all files associated with a bill.
        """
        bill = self.get_object()
        files = FileBill.objects.filter(access_to_model=bill)
        serializer = FileBillSerializer(
            files, 
            many=True, 
            context={'request': request}
        )
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def upload_file(self, request, pk=None):
        """
        Upload a file associated with a bill.
        """
        bill = self.get_object()
        serializer = FileBillSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            serializer.save(access_to_model=bill)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 