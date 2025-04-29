from django.http import JsonResponse, HttpResponse
from django.db import connections
from django.db.utils import OperationalError
from core.utils.container_health import get_container_health_status


def health_check(request):
    """
    Performs a health check for the Django application.
    Verifies database connectivity and other system components.
    
    Returns:
        200 OK if the application is healthy
        500 Server Error if any component is unhealthy
    """
    # Get comprehensive health status
    is_healthy, status_details = get_container_health_status()
    
    # Create response with overall status
    response = {
        'status': 'healthy' if is_healthy else 'unhealthy',
        'details': status_details
    }
    
    # Return appropriate status code based on health
    status_code = 200 if is_healthy else 500
    
    return JsonResponse(response, status=status_code) 