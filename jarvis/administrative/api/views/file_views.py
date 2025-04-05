"""
File views for Administrative API.
"""

from rest_framework import viewsets, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters import rest_framework as filters
from administrative.models import File
from administrative.api.serializers.file_serializers import FileSerializer


class FileFilter(filters.FilterSet):
    """Filter for File queryset."""
    
    name = filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = File
        fields = ['name']


class FileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the File model.
    
    This viewset provides `list`, `create`, `retrieve`, `update`, and `destroy` actions.
    """
    
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = FileFilter
    parser_classes = [MultiPartParser, FormParser] 