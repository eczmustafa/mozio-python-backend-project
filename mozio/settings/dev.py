from .common import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-2)x29irl*+yexp$8!z@g*+n+7vvq7b%%lo71+@zzh3!nuq-_b9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': "mozio",
        'USER': "user",
        'PASSWORD': "1234",
        'HOST': 'db',
        'PORT': 5432,
    },
    'test': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': "test_mozio",
        'USER': "user",
        'PASSWORD': "1234",
        'HOST': 'localhost',
        'PORT': 5432,
    },
}