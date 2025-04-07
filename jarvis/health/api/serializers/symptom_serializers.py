"""
Symptom serializers for the Health API.
"""
from rest_framework import serializers
from health.models import Symptom, FileSymptom


class SymptomSerializer(serializers.ModelSerializer):
    """
    Serializer for the Symptom model.
    """
    url = serializers.HyperlinkedIdentityField(
        view_name='symptom-detail',
        lookup_field='pk'
    )
    
    class Meta:
        model = Symptom
        fields = [
            'id', 'url', 'name', 'child', 'adult', 
            'products', 'comments'
        ]
        read_only_fields = ['id', 'url']


class SymptomDetailSerializer(SymptomSerializer):
    """
    Detailed serializer for the Symptom model.
    Includes related files and products detail.
    """
    files = serializers.SerializerMethodField()
    products_detail = serializers.SerializerMethodField()

    class Meta(SymptomSerializer.Meta):
        fields = SymptomSerializer.Meta.fields + ['files', 'products_detail']

    def get_files(self, obj):
        """
        Get the files associated with the symptom.
        """
        from .file_serializers import FileSymptomSerializer
        files = FileSymptom.objects.filter(access_to_model=obj)
        return FileSymptomSerializer(
            files, 
            many=True,
            context=self.context
        ).data
        
    def get_products_detail(self, obj):
        """
        Get detailed information about associated products.
        """
        from .product_serializers import ProductSerializer
        return ProductSerializer(
            obj.products.all(),
            many=True,
            context=self.context
        ).data 