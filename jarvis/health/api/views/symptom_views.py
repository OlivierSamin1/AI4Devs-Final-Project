"""
Symptom views for the Health API.
"""
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as filters

from health.models import Symptom, FileSymptom
from ..serializers.symptom_serializers import SymptomSerializer, SymptomDetailSerializer
from ..serializers.file_serializers import FileSymptomSerializer
from ..serializers.product_serializers import ProductSerializer


class SymptomFilter(filters.FilterSet):
    """
    Filter for Symptom queryset.
    """
    name = filters.CharFilter(lookup_expr='icontains')
    child = filters.BooleanFilter()
    adult = filters.BooleanFilter()
    product = filters.NumberFilter(field_name='products')
    
    class Meta:
        model = Symptom
        fields = ['name', 'child', 'adult', 'product']


class SymptomViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Symptoms.
    """
    queryset = Symptom.objects.all()
    serializer_class = SymptomSerializer
    filterset_class = SymptomFilter
    permission_classes = [permissions.AllowAny]  # Allow any access for debugging
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SymptomDetailSerializer
        return self.serializer_class
    
    @action(detail=True, methods=['get'])
    def files(self, request, pk=None):
        """
        Get all files associated with a symptom.
        """
        symptom = self.get_object()
        files = FileSymptom.objects.filter(access_to_model=symptom)
        serializer = FileSymptomSerializer(
            files, 
            many=True, 
            context={'request': request}
        )
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        """
        Get all products associated with a symptom.
        """
        symptom = self.get_object()
        products = symptom.products.all()
        serializer = ProductSerializer(
            products, 
            many=True, 
            context={'request': request}
        )
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def upload_file(self, request, pk=None):
        """
        Upload a file associated with a symptom.
        """
        symptom = self.get_object()
        serializer = FileSymptomSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            serializer.save(access_to_model=symptom)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 