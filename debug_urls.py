"""
Debug URLs for the Jarvis project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken import views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.http import HttpResponse

def debug_view(request):
    """An extremely simple view for debugging."""
    return HttpResponse("Hello from Django!", content_type="text/plain")

@api_view(['GET'])
@permission_classes([AllowAny])
def api_debug_view(request):
    """A simple DRF API view for debugging."""
    return Response({
        'status': 'OK',
        'message': 'API is working'
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    
    # Debug endpoints
    path('debug/', debug_view),
    path('api/debug/', api_debug_view),
    
    # API endpoints
    path('api/administrative/', include('administrative.api.urls')),
    path('api/health/', include('health.api.urls')),
    path('api-token-auth/', views.obtain_auth_token),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 