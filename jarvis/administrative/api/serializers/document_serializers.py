"""
Document serializers for Administrative API.
"""

from rest_framework import serializers
from administrative.models import Document, FileDocument


class DocumentSerializer(serializers.ModelSerializer):
    """Serializer for the Document model."""
    
    file_count = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(
        view_name='document-detail',
        lookup_field='pk'
    )
    
    class Meta:
        model = Document
        fields = [
            'id', 'user', 'name', 'type', 'comment', 
            'file_count', 'url'
        ]
        read_only_fields = ['id', 'file_count']
    
    def get_file_count(self, obj):
        """Get the number of files associated with this document."""
        return obj.document_files.count()


class DocumentFileSerializer(serializers.ModelSerializer):
    """Serializer for listing files associated with a document."""
    
    class Meta:
        model = FileDocument
        fields = ['id', 'name', 'content']
        read_only_fields = ['id'] 