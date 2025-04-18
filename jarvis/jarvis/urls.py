"""
URL configuration for jarvis project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken import views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import logging
from django.http import HttpResponse

logger = logging.getLogger(__name__)

def super_basic_test(request):
    """An absolute minimal view that just returns a string with no dependencies."""
    return HttpResponse("OK", content_type="text/plain")

def basic_test(request):
    """A basic view that returns a simple HTTP response for debugging."""
    try:
        logger.info(f"Basic test accessed: {request.path}, Method: {request.method}")
        logger.info(f"Request headers: {request.headers}")
        logger.info(f"Request META: {request.META}")
        return HttpResponse("Basic test view is working", content_type="text/plain")
    except Exception as e:
        logger.error(f"Error in basic_test: {str(e)}")
        return HttpResponse(f"Error: {str(e)}", content_type="text/plain", status=500)

@api_view(['GET'])
def api_root(request):
    logger.info(f"API root accessed: {request.path}, Method: {request.method}, Headers: {request.headers}")
    return Response({
        'status': 'OK',
        'message': 'Jarvis API is running'
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def api_test(request):
    logger.info(f"API test accessed: {request.path}, Method: {request.method}, Headers: {request.headers}")
    try:
        return Response({
            'status': 'OK',
            'message': 'API test endpoint is working'
        })
    except Exception as e:
        logger.error(f"Error in api_test: {str(e)}")
        raise

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    
    # Basic test views
    path('super-basic-test/', super_basic_test),
    path('basic-test/', basic_test),
    
    # API root endpoint
    path('', api_root),
    
    # Test API endpoint - add multiple versions to test different URL patterns
    path('api/test/', api_test),
    path('test/', api_test),  # Try without the /api prefix
    
    # API endpoints
    path('api/administrative/', include('administrative.api.urls')),
    path('api/health/', include('health.api.urls')),
    path('api-token-auth/', views.obtain_auth_token),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 