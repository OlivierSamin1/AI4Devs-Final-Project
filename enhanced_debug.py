#!/usr/bin/env python3
import os
import sys

# Path to the settings file
settings_path = '/app/jarvis/settings.py'

# Check if file exists
if not os.path.exists(settings_path):
    print(f"Error: Settings file not found at {settings_path}")
    sys.exit(1)

# Read the current settings file
with open(settings_path, 'r') as f:
    settings_content = f.read()

# Add verbose logging configuration
logging_config = """
# Enhanced logging for debugging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.server': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
"""

if 'LOGGING = {' not in settings_content:
    settings_content += logging_config

# Make sure DEBUG is True
if 'DEBUG = False' in settings_content:
    settings_content = settings_content.replace('DEBUG = False', 'DEBUG = True')

# Write the updated settings back to the file
with open(settings_path, 'w') as f:
    f.write(settings_content)

# Create a diagnostic script
diagnostic_script = """#!/usr/bin/env python3
import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jarvis.settings')
django.setup()

from django.urls import get_resolver
from django.conf import settings

# Print installed apps
print("\\n=== INSTALLED APPS ===")
for app in settings.INSTALLED_APPS:
    print(f"- {app}")

# Print URL patterns
print("\\n=== URL PATTERNS ===")
resolver = get_resolver()
for pattern in resolver.url_patterns:
    print(f"- {pattern.pattern}")

print("\\n=== DEBUG MODE ===")
print(f"DEBUG: {settings.DEBUG}")

print("\\n=== ALLOWED HOSTS ===")
print(f"ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")

print("\\n=== REST FRAMEWORK CONFIG ===")
if hasattr(settings, 'REST_FRAMEWORK'):
    print(f"REST_FRAMEWORK: {settings.REST_FRAMEWORK}")
else:
    print("REST_FRAMEWORK is not defined")

print("\\nDiagnostic complete!")
"""

# Write the diagnostic script
diagnostic_path = '/app/diagnostics.py'
with open(diagnostic_path, 'w') as f:
    f.write(diagnostic_script)
os.chmod(diagnostic_path, 0o755)

# Create a standalone test view file
test_view_file = """from django.http import HttpResponse

def test_view(request):
    return HttpResponse("Test view successful!")
"""

test_view_path = '/app/jarvis/test_view.py'
with open(test_view_path, 'w') as f:
    f.write(test_view_file)

# Update urls.py to include the standalone test view
urls_path = '/app/jarvis/urls.py'
if os.path.exists(urls_path):
    with open(urls_path, 'r') as f:
        urls_content = f.read()
    
    # Add import for the standalone test view
    if 'from jarvis.test_view import test_view' not in urls_content:
        if 'from django.urls import' in urls_content:
            urls_content = urls_content.replace('from django.urls import', 'from django.urls import\nfrom jarvis.test_view import test_view')
    
    # Add the test URL pattern
    if '"test/"' not in urls_content and "'test/'" not in urls_content:
        if 'urlpatterns = [' in urls_content:
            urls_content = urls_content.replace('urlpatterns = [', 'urlpatterns = [\n    path("test/", test_view),')
    
    with open(urls_path, 'w') as f:
        f.write(urls_content)

print("Enhanced debugging setup complete!") 