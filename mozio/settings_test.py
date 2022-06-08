from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': "test_mozio",
        'USER': "user",
        'PASSWORD': "1234",
        'HOST': 'localhost',
        'PORT': 5432,
    },
}