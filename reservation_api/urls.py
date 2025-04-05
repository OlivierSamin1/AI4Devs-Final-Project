from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'assets', views.AssetViewSet)
router.register(r'platforms', views.RentalPlatformViewSet)
router.register(r'reservations', views.ReservationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('fuerteventura-reservations/', views.get_fuerteventura_reservations, name='fuerteventura-reservations'),
] 