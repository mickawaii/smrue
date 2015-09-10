"""
Django settings for smrue project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import socket
import dj_database_url
from django.core.wsgi import get_wsgi_application
from datetime import timedelta
import djcelery

# import pdb; pdb.set_trace()
djcelery.setup_loader()
BROKER_URL = "amqp://hcsdnhkh:VN77lxrzyQ2QHk2VzEwkWTtrjno9hnlY@owl.rmq.cloudamqp.com/hcsdnhkh"
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+2viif%shj@r*$g^h$-6c^pbclg1ieq)xyq78yd9o=ygwke0jb'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

LOGIN_URL = '/login/'

LOGOUT_URL = '/logout/'

LOGIN_REDIRECT_URL = '/'

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = [".herokuapp.com"]

# Application definition

INSTALLED_APPS = (
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'smrue',
	'equipment',
	'consumption',
	'goal',
	'sensor',
	'aes_rate',
	'configuration',
	'djcelery',
)

MIDDLEWARE_CLASSES = (
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'smrue.urls'

WSGI_APPLICATION = 'smrue.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

# DATABASES = {
# 	'default': {
# 		'ENGINE': 'django.db.backends.sqlite3',
# 		'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
# 	}
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'df92jg90v64ufb',                      
        'USER': 'kawmralupavplb',
        'PASSWORD': 'LO9AMno_SHFuIM7IeSQGLajp2z',
        'HOST': 'ec2-54-83-18-87.compute-1.amazonaws.com',
        'PORT': '5432',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'pt-BR'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
	os.path.join(BASE_DIR, 'static'),
)

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'melhortcc2015@gmail.com'
EMAIL_HOST_PASSWORD = 'henriquemi'
DEFAULT_FROM_EMAIL = 'melhortcc2015@gmail.com'
EMAIL_PORT = 587

if 'BASE_IRI' in os.environ:

	DEBUG = TEMPLATE_DEBUG = True

	DATABASES = {'default': dj_database_url.config(default='postgres://tkihlhiauawvvx:SlfzPvh1rai6YSp6_lmckX3KfQ@ec2-54-227-249-165.compute-1.amazonaws.com:5432/d312ostfbfevth')}

#Celery configuration (tasks) - http://celery.readthedocs.org/en/latest/userguide/periodic-tasks.html
# CELERY_TIMEZONE = 'America/Sao_Paulo'
	#Toda vez que o timezone muda, rode:
	# $ python manage.py shell
	# >>> from djcelery.models import PeriodicTask
	# >>> PeriodicTask.objects.update(last_run_at=None)
# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'
CELERYBEAT_SCHEDULE = {
    'add-every-1-days': {
        'task': 'smrue.tasks.add',
        'schedule': timedelta(hours=6),
        'args': ()
    },
}