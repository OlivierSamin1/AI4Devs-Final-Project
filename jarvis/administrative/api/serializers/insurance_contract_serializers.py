"""
Insurance Contract serializers for Administrative API.
"""

from rest_framework import serializers
from administrative.models import InsuranceContract, FileInsuranceContract
from administrative.api.serializers.insurance_company_serializers import InsuranceCompanySerializer


class InsuranceContractSerializer(serializers.ModelSerializer):
    """Serializer for the InsuranceContract model."""
    
    company_details = InsuranceCompanySerializer(source='company', read_only=True)
    url = serializers.HyperlinkedIdentityField(
        view_name='insurance-contract-detail',
        lookup_field='pk'
    )
    file_count = serializers.SerializerMethodField()
    
    class Meta:
        model = InsuranceContract
        fields = [
            'id', 'company', 'company_details', 'type', 
            'real_estate_asset', 'transportation_asset', 'person',
            'contract_number', 'starting_date', 'ending_date',
            'is_insurance_active', 'personal_email_used',
            'annual_price', 'coverage', 'file_count', 'url'
        ]
        read_only_fields = ['id', 'company_details', 'file_count']
    
    def get_file_count(self, obj):
        """Get the number of files associated with this contract."""
        return obj.insurance_contract_files.count()


class ContractFileSerializer(serializers.ModelSerializer):
    """Serializer for listing files associated with a contract."""
    
    class Meta:
        model = FileInsuranceContract
        fields = ['id', 'name', 'content']
        read_only_fields = ['id'] 