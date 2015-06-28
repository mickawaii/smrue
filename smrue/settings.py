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
# from whitenoise.django import DjangoWhiteNoise

PRODUCTION_HOST_NAME = "db32a008-53a1-4a81-8ac9-06365e391753"

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+2viif%shj@r*$g^h$-6c^pbclg1ieq)xyq78yd9o=ygwke0jb'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


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
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'pt-BR'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

# STATIC_URL = '/static/'

# STATIC_ROOT = 'static/'

STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'
MEDIA_ROOT = 'media'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

if socket.gethostname() == PRODUCTION_HOST_NAME:
    DEBUG = TEMPLATE_DEBUG = False

    DATABASES = {
        'default': {
            'ENGINE': 'django_postgrespool', 
            'NAME': 'd312ostfbfevth',  
            'USER': 'tkihlhiauawvvx',
            'PASSWORD': 'SlfzPvh1rai6YSp6_lmckX3KfQ',
            'HOST': 'ec2-54-227-249-165.compute-1.amazonaws.com',  
            'PORT': '5432', 
        }
    }

    DATABASES['default'] = dj_database_url.config()
    STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
