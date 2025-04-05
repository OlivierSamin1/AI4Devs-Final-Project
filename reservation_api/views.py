from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from datetime import datetime
from .models import Asset, RentalPlatform, Reservation
from .serializers import AssetSerializer, RentalPlatformSerializer, ReservationSerializer

class AssetViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer

class RentalPlatformViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RentalPlatform.objects.all()
    serializer_class = RentalPlatformSerializer

class ReservationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_fuerteventura_reservations(request):
    month = request.query_params.get('month', '2')
    year = request.query_params.get('year', '2025')
    
    try:
        # Find the FuerteVentura asset - adjust this query to match your data
        asset = Asset.objects.filter(nickname__icontains='fuerte').first()
        if not asset:
            return Response({'error': 'FuerteVentura asset not found'}, status=404)
        
        # Get reservations for the specified month and year
        reservations = Reservation.objects.filter(
            Q(asset=asset) &
            (
                # Reservations that start in the target month
                Q(entry_date__month=month, entry_date__year=year) |
                # Reservations that end in the target month
                Q(end_date__month=month, end_date__year=year)
            )
        ).order_by('entry_date')
        
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)
        
    except Exception as e:
        return Response({'error': str(e)}, status=500) 