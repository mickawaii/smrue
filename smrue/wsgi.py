"""
WSGI config for smrue project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smrue.settings")

from django.core.wsgi import get_wsgi_application
from django.conf import settings
from whitenoise.django import DjangoWhiteNoise
import socket

# DEVELOPMENT
application = get_wsgi_application()
application = DjangoWhiteNoise(application)

# if socket.gethostname() == settings.PRODUCTION_HOST_NAME:
	# from dj_static import Cling
	# application = Cling(get_wsgi_application())


