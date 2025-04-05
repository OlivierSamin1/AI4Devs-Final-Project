"""
Insurance Contract views for Administrative API.
"""

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as filters
from administrative.models import InsuranceContract, FileInsuranceContract
from administrative.api.serializers.insurance_contract_serializers import (
    InsuranceContractSerializer, ContractFileSerializer
)
from administrative.api.serializers.file_serializers import FileUploadSerializer


class InsuranceContractFilter(filters.FilterSet):
    """Filter for InsuranceContract queryset."""
    
    type = filters.CharFilter(lookup_expr='exact')
    active = filters.BooleanFilter(field_name='is_insurance_active')
    user = filters.NumberFilter(field_name='person')
    
    class Meta:
        model = InsuranceContract
        fields = ['company', 'type', 'is_insurance_active', 'person']


class InsuranceContractViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the InsuranceContract model.
    
    This viewset provides `list`, `create`, `retrieve`, `update`, and `destroy` actions.
    """
    
    queryset = InsuranceContract.objects.all()
    serializer_class = InsuranceContractSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = InsuranceContractFilter
    
    @action(detail=True, methods=['get'])
    def files(self, request, pk=None):
        """Get the files associated with this contract."""
        contract = self.get_object()
        files = FileInsuranceContract.objects.filter(access_to_model=contract)
        serializer = ContractFileSerializer(files, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def upload_file(self, request, pk=None):
        """Upload a file for this contract."""
        contract = self.get_object()
        serializer = FileUploadSerializer(data=request.data)
        
        if serializer.is_valid():
            file_contract = FileInsuranceContract.objects.create(
                name=serializer.validated_data.get('name', ''),
                content=serializer.validated_data['content'],
                access_to_model=contract
            )
            file_serializer = ContractFileSerializer(file_contract, context={'request': request})
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContractFileListView(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for listing files associated with a contract.
    """
    
    serializer_class = ContractFileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Get files for the specified contract."""
        contract_id = self.kwargs.get('contract_id')
        return FileInsuranceContract.objects.filter(access_to_model_id=contract_id) 