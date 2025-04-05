from rest_framework import serializers
from .models import Asset, RentalPlatform, Reservation

class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = '__all__'

class RentalPlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentalPlatform
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    platform_name = serializers.ReadOnlyField(source='platform.name')
    asset_name = serializers.ReadOnlyField(source='asset.nickname')
    
    class Meta:
        model = Reservation
        fields = [
            'id', 'asset_id', 'asset_name', 'platform_id', 'platform_name',
            'reservation_number', 'entry_date', 'number_of_nights', 'end_date',
            'renting_person_full_name', 'price', 'created_at'
        ] 