import os

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smrue.settings')

from celery import task
import django

from celery import Celery

from django.conf import settings
django.setup()

from aes_rate.models import AESRate

app = Celery()

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

from django.core.wsgi import get_wsgi_application
from django.conf import settings
from whitenoise.django import DjangoWhiteNoise
import socket

application = get_wsgi_application()
application = DjangoWhiteNoise(application)

@task()
def add():
	print("The worker has was called!")
	AESRate.update_info()
