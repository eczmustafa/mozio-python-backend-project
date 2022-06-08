from decimal import Decimal

from django.db import transaction
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import Provider, ServiceArea


class ProviderBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = [
            "id",
            "name",
        ]


class ServiceAreaSearchSerializer(GeoFeatureModelSerializer):
    # The name of the polygon, provider's name, and price should be returned for each polygon
    provider = ProviderBasicSerializer(read_only=True)

    class Meta:
        model = ServiceArea
        fields = ["id", "name", "provider", "price"]
        geo_field = "geojson"


class ServiceAreaSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = ServiceArea
        fields = ["id", "provider", "name", "price"]
        geo_field = "geojson"


class ProviderSerializer(serializers.ModelSerializer):
    serviceareas = ServiceAreaSerializer(many=True, read_only=True)
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Provider
        fields = [
            "id",
            "name",
            "email",
            "phone_number",
            "language",
            "currency",
            "serviceareas",
        ]
