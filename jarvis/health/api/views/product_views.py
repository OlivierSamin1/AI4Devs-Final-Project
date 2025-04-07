"""
Product views for the Health API.
"""
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as filters

from health.models import Product, FileProduct
from ..serializers.product_serializers import ProductSerializer, ProductDetailSerializer
from ..serializers.file_serializers import FileProductSerializer


class ProductFilter(filters.FilterSet):
    """
    Filter for Product queryset.
    """
    name = filters.CharFilter(lookup_expr='icontains')
    natural = filters.BooleanFilter()
    child_use = filters.BooleanFilter()
    adult_use = filters.BooleanFilter()
    
    class Meta:
        model = Product
        fields = ['name', 'natural', 'child_use', 'adult_use']


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Products.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = ProductFilter
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return self.serializer_class
    
    @action(detail=True, methods=['get'])
    def files(self, request, pk=None):
        """
        Get all files associated with a product.
        """
        product = self.get_object()
        files = FileProduct.objects.filter(access_to_model=product)
        serializer = FileProductSerializer(
            files, 
            many=True, 
            context={'request': request}
        )
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def upload_file(self, request, pk=None):
        """
        Upload a file associated with a product.
        """
        product = self.get_object()
        serializer = FileProductSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            serializer.save(access_to_model=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 