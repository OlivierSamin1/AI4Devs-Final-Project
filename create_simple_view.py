#!/usr/bin/env python3
import os

# Create a standalone test view file
simple_view_content = """from django.http import HttpResponse

def direct_test_view(request):
    return HttpResponse("Direct test view successful!")
"""

simple_view_path = '/app/jarvis/simple_view.py'
with open(simple_view_path, 'w') as f:
    f.write(simple_view_content)

# Update urls.py to include the direct test view
urls_path = '/app/jarvis/urls.py'
with open(urls_path, 'r') as f:
    urls_content = f.read()

# Add import for the simple view
if 'from jarvis.simple_view import direct_test_view' not in urls_content:
    urls_content = urls_content.replace(
        'from django.urls import path, include',
        'from django.urls import path, include\nfrom jarvis.simple_view import direct_test_view'
    )

# Add URL pattern for the direct test view
if 'direct-test/' not in urls_content:
    urls_content = urls_content.replace(
        'urlpatterns = [',
        'urlpatterns = [\n    path("direct-test/", direct_test_view),'
    )

with open(urls_path, 'w') as f:
    f.write(urls_content)

print("Simple test view added successfully!") 