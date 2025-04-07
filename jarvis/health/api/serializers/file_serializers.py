"""
File serializers for the Health API.
"""
from rest_framework import serializers
from health.models import (
    File, FileBill, FileProduct, FileSymptom,
    Bill, Product, Symptom
)


class FileSerializer(serializers.ModelSerializer):
    """
    Base serializer for the File model.
    """
    url = serializers.HyperlinkedIdentityField(
        view_name='file-detail',
        lookup_field='pk'
    )
    
    class Meta:
        model = File
        fields = ['id', 'url', 'name', 'content']
        read_only_fields = ['id', 'url']


class FileBillSerializer(FileSerializer):
    """
    Serializer for the FileBill model.
    """
    bill_id = serializers.PrimaryKeyRelatedField(
        queryset=Bill.objects.all(),
        source='access_to_model',
        write_only=True
    )
    
    class Meta(FileSerializer.Meta):
        model = FileBill
        fields = FileSerializer.Meta.fields + ['access_to_model', 'bill_id']
        read_only_fields = FileSerializer.Meta.read_only_fields + ['access_to_model']


class FileProductSerializer(FileSerializer):
    """
    Serializer for the FileProduct model.
    """
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='access_to_model',
        write_only=True
    )
    
    class Meta(FileSerializer.Meta):
        model = FileProduct
        fields = FileSerializer.Meta.fields + ['access_to_model', 'product_id']
        read_only_fields = FileSerializer.Meta.read_only_fields + ['access_to_model']


class FileSymptomSerializer(FileSerializer):
    """
    Serializer for the FileSymptom model.
    """
    symptom_id = serializers.PrimaryKeyRelatedField(
        queryset=Symptom.objects.all(),
        source='access_to_model',
        write_only=True
    )
    
    class Meta(FileSerializer.Meta):
        model = FileSymptom
        fields = FileSerializer.Meta.fields + ['access_to_model', 'symptom_id']
        read_only_fields = FileSerializer.Meta.read_only_fields + ['access_to_model'] 