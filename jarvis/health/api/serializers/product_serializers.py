"""
Product serializers for the Health API.
"""
from rest_framework import serializers
from health.models import Product, FileProduct


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.
    """
    url = serializers.HyperlinkedIdentityField(
        view_name='product-detail',
        lookup_field='pk'
    )
    
    class Meta:
        model = Product
        fields = [
            'id', 'url', 'name', 'natural', 'child_use', 'adult_use',
            'min_age', 'source_info', 'date_info', 'composition',
            'interests', 'comments'
        ]
        read_only_fields = ['id', 'url']


class ProductDetailSerializer(ProductSerializer):
    """
    Detailed serializer for the Product model.
    Includes related files.
    """
    files = serializers.SerializerMethodField()

    class Meta(ProductSerializer.Meta):
        fields = ProductSerializer.Meta.fields + ['files']

    def get_files(self, obj):
        """
        Get the files associated with the product.
        """
        from .file_serializers import FileProductSerializer
        files = FileProduct.objects.filter(access_to_model=obj)
        return FileProductSerializer(
            files, 
            many=True,
            context=self.context
        ).data 