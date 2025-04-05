"""
Insurance Company serializers for Administrative API.
"""

from rest_framework import serializers
from administrative.models import InsuranceCompany


class InsuranceCompanySerializer(serializers.ModelSerializer):
    """Serializer for the InsuranceCompany model."""
    
    url = serializers.HyperlinkedIdentityField(
        view_name='insurance-company-detail',
        lookup_field='pk'
    )
    contract_count = serializers.SerializerMethodField()
    
    class Meta:
        model = InsuranceCompany
        fields = [
            'id', 'name', 'phone_number', 'site_app_company',
            'contract_count', 'url'
        ]
        read_only_fields = ['id', 'contract_count']
    
    def get_contract_count(self, obj):
        """Get the number of contracts associated with this company."""
        return obj.contract.count() if hasattr(obj, 'contract') else 0 