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
from django.http import HttpResponse

def super_basic_test(request):
    return HttpResponse('OK', content_type='text/plain')

def basic_test(request):
    return HttpResponse('Basic test view is working', content_type='text/plain')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    
    # Test endpoints
    path('super-basic-test/', super_basic_test),
    path('basic-test/', basic_test),
    
    # API endpoints
    path('api/administrative/', include('administrative.api.urls')),
    path('api/health/', include('health.api.urls')),
    path('api-token-auth/', views.obtain_auth_token),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 