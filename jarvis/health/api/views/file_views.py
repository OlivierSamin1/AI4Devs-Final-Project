"""
File views for the Health API.
"""
from rest_framework import viewsets, permissions, status
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters import rest_framework as filters

from health.models import (
    File, FileBill, FileProduct, FileSymptom
)
from ..serializers.file_serializers import (
    FileSerializer, FileBillSerializer, 
    FileProductSerializer, FileSymptomSerializer
)


class FileFilter(filters.FilterSet):
    """
    Filter for File queryset.
    """
    name = filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = File
        fields = ['name']


class FileViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Files.
    """
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    filterset_class = FileFilter


class FileBillViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Bill Files.
    """
    queryset = FileBill.objects.all()
    serializer_class = FileBillSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    filterset_class = FileFilter


class FileProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Product Files.
    """
    queryset = FileProduct.objects.all()
    serializer_class = FileProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    filterset_class = FileFilter


class FileSymptomViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Symptom Files.
    """
    queryset = FileSymptom.objects.all()
    serializer_class = FileSymptomSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    filterset_class = FileFilter 