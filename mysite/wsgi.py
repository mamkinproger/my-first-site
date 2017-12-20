"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

application = get_wsgi_application()

# import os
# import sys
# sys.path.insert(0, 'user\Desktop\profile-model\mysite')
# sys.path.insert(0, 'user\Desktop\profile-model')
# os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
# import django.core.handlers.wsgi
# application = django.core.handlers.wsgi.WSGIHandler()

