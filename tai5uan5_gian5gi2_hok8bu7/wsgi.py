"""
WSGI config for tai5uan5_gian5gi2_hok8bu7 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tai5uan5_gian5gi2_hok8bu7.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
