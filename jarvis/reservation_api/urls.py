from django.urls import path
from . import views

urlpatterns = [
    path('fuerteventura-reservations/', views.get_fuerteventura_reservations, name='fuerteventura-reservations'),
    # Add other URL patterns as needed
]
