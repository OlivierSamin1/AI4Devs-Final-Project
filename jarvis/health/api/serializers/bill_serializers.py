"""
Bill serializers for the Health API.
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from health.models import Bill, FileBill


class UserSerializer(serializers.ModelSerializer):
    """
    Simple User serializer for nested representations.
    """
    class Meta:
        model = User
        fields = ['id', 'username']


class BillSerializer(serializers.ModelSerializer):
    """
    Serializer for the Bill model.
    """
    url = serializers.HyperlinkedIdentityField(
        view_name='bill-detail',
        lookup_field='pk'
    )
    client_name = UserSerializer(read_only=True)
    client_name_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='client_name',
        write_only=True
    )
    
    class Meta:
        model = Bill
        fields = [
            'id', 'url', 'company_name', 'client_name', 'client_name_id',
            'bill_name', 'date', 'total_price', 'is_paid', 'is_asked_by_us'
        ]
        read_only_fields = ['id', 'url']


class BillDetailSerializer(BillSerializer):
    """
    Detailed serializer for the Bill model.
    Includes related files.
    """
    files = serializers.SerializerMethodField()

    class Meta(BillSerializer.Meta):
        fields = BillSerializer.Meta.fields + ['files']

    def get_files(self, obj):
        """
        Get the files associated with the bill.
        """
        from .file_serializers import FileBillSerializer
        files = FileBill.objects.filter(access_to_model=obj)
        return FileBillSerializer(
            files, 
            many=True,
            context=self.context
        ).data 