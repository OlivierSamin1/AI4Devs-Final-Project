from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health_check, name='api_health_check'),
    path('chat/', views.chat, name='chat'),
] 