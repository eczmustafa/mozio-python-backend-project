import pytest
from api.models import Provider, ServiceArea
from django.contrib.gis.geos import GEOSGeometry
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestSearchServiceArea:
    def setup_method(self, test_method):
        provider = Provider()
        provider.name = "abc provider"
        provider.email = "abc@provider.com"
        provider.phone_number = "+123404"
        provider.language = "EN"
        provider.currency = "EUR"
        provider.save()
        self.provider = provider

        service_area = ServiceArea()
        service_area.provider = provider
        service_area.name = "test"
        service_area.price = 100
        service_area.geojson = GEOSGeometry(
            "POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))"
        )
        service_area.save()
        self.service_area = service_area

    def teardown_method(self, test_method):
        ...

    def test_search_service_and_find_an_existing_one(self):
        client = APIClient()
        response = client.get("/api/search/", QUERY_STRING="latitude=25&longitude=15")
        assert "features" in response.data
        assert len(response.data["features"]) == 1

    def test_search_a_non_existing_area_service(self):
        client = APIClient()
        response = client.get("/api/search/", QUERY_STRING="latitude=-25&longitude=-15")
        assert "features" in response.data
        assert len(response.data["features"]) == 0
