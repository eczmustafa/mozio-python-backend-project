from uuid import uuid4

from django.contrib.gis.db import models as gis_models
from django.db import models
from rest_framework import serializers

# Create your models here.


class Provider(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=20)
    language = models.CharField(max_length=20)
    currency = models.CharField(max_length=3)  # iso currency code


class ServiceArea(models.Model):
    provider = models.ForeignKey(
        Provider, on_delete=models.PROTECT, related_name="serviceareas", default=0
    )
    name = models.CharField(max_length=255)
    price = models.DecimalField(
        max_digits=6, decimal_places=2
    )  # avoid floats for prices
    geojson = gis_models.PolygonField()
