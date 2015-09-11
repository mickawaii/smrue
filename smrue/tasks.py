from celery import task
from aes_rate.models import AESRate

import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smrue.settings')


from django.conf import settings
configure()
django.setup()
if not setting.configured:
	setting.configure('DJANGO_SETTINGS_MODULE', 'smrue.settings')

app = Celery()

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@task()
def add():
	print("The worker has was called!")
	AESRate.update_info()