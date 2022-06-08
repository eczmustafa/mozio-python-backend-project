from decimal import Decimal

from django.db import transaction
from rest_framework import serializers
from rest_framework.views import exception_handler
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
    provider=serializers.StringRelatedField()
    class Meta:
        model = ServiceArea
        fields = ["id", "provider", "name", "price"]
        geo_field = "geojson"
    
    def save(self, **kwargs):
        provider_id = self.context["provider_id"]

        self.instance = ServiceArea.objects.create(
            provider_id=provider_id, **self.validated_data
        )

        return self.instance


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
