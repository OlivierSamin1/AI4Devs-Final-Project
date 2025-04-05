from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import HollydaysReservation, Asset
from .serializers import ReservationSerializer

# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_fuerteventura_reservations(request):
    month = request.query_params.get('month', '2')
    year = request.query_params.get('year', '2025')
    
    try:
        asset = Asset.objects.filter(nickname__icontains='fuerte').first()
        if not asset:
            return Response({'error': 'FuerteVentura asset not found'}, status=404)
        
        reservations = HollydaysReservation.objects.filter(
            Q(asset=asset) &
            (
                Q(entry_date__month=month, entry_date__year=year) |
                Q(end_date__month=month, end_date__year=year)
            )
        ).order_by('entry_date')
        
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)
        
    except Exception as e:
        return Response({'error': str(e)}, status=500)
