"""
Document views for Administrative API.
"""

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as filters
from administrative.models import Document, FileDocument
from administrative.api.serializers.document_serializers import (
    DocumentSerializer, DocumentFileSerializer
)
from administrative.api.serializers.file_serializers import FileUploadSerializer


class DocumentFilter(filters.FilterSet):
    """Filter for Document queryset."""
    
    type = filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = Document
        fields = ['user', 'type']


class DocumentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the Document model.
    
    This viewset provides `list`, `create`, `retrieve`, `update`, and `destroy` actions.
    """
    
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = DocumentFilter
    
    @action(detail=True, methods=['get'])
    def files(self, request, pk=None):
        """Get the files associated with this document."""
        document = self.get_object()
        files = FileDocument.objects.filter(access_to_model=document)
        serializer = DocumentFileSerializer(files, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def upload_file(self, request, pk=None):
        """Upload a file for this document."""
        document = self.get_object()
        serializer = FileUploadSerializer(data=request.data)
        
        if serializer.is_valid():
            file_document = FileDocument.objects.create(
                name=serializer.validated_data.get('name', ''),
                content=serializer.validated_data['content'],
                access_to_model=document
            )
            file_serializer = DocumentFileSerializer(file_document, context={'request': request})
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DocumentFileListView(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for listing files associated with a document.
    """
    
    serializer_class = DocumentFileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Get files for the specified document."""
        document_id = self.kwargs.get('document_id')
        return FileDocument.objects.filter(access_to_model_id=document_id) 