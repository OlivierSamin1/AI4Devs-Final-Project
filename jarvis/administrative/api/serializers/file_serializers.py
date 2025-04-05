"""
File serializers for Administrative API.
"""

from rest_framework import serializers
from administrative.models import File, FileDocument, FileInsuranceContract


class FileSerializer(serializers.ModelSerializer):
    """Serializer for the base File model."""
    
    url = serializers.HyperlinkedIdentityField(
        view_name='file-detail',
        lookup_field='pk'
    )
    content_url = serializers.SerializerMethodField()
    
    class Meta:
        model = File
        fields = ['id', 'name', 'content', 'content_url', 'url']
        read_only_fields = ['id', 'content_url']
    
    def get_content_url(self, obj):
        """Get the URL for the file content."""
        if obj.content and hasattr(obj.content, 'url'):
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.content.url)
        return None


class FileDocumentSerializer(FileSerializer):
    """Serializer for the FileDocument model."""
    
    class Meta(FileSerializer.Meta):
        model = FileDocument
        fields = FileSerializer.Meta.fields + ['access_to_model']


class FileInsuranceContractSerializer(FileSerializer):
    """Serializer for the FileInsuranceContract model."""
    
    class Meta(FileSerializer.Meta):
        model = FileInsuranceContract
        fields = FileSerializer.Meta.fields + ['access_to_model']


class FileUploadSerializer(serializers.Serializer):
    """Serializer for file upload."""
    
    name = serializers.CharField(max_length=100, required=False)
    content = serializers.FileField(required=True)
    
    def validate_content(self, value):
        """Validate the file content."""
        # Add file size validation
        if value.size > 10 * 1024 * 1024:  # 10MB limit
            raise serializers.ValidationError("File size should not exceed 10MB.")
        return value 