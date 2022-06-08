import os
from .common import *
import dj_database_url

DEBUG = False

SECRET_KEY = os.environ["SECRET_KEY"]

ALLOWED_HOSTS = ["ec2-3-73-79-152.eu-central-1.compute.amazonaws.com"]

DATABASES = {
    "default": dj_database_url.config(),
}
DATABASES["default"]["ENGINE"] = "django.contrib.gis.db.backends.postgis"
