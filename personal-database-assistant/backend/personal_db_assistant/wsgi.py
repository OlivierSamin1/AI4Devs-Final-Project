"""
WSGI config for personal_db_assistant project.

It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'personal_db_assistant.settings')

application = get_wsgi_application() 