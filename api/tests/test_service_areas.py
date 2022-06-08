from rest_framework import status
from rest_framework.test import APIClient
from api.models import Provider, ServiceArea
import pytest


@pytest.mark.django_db
class TestCreateServiceArea:
    def setup_method(self, test_method):
        provider = Provider()
        provider.name = "abc provider"
        provider.email = "abc@provider.com"
        provider.phone_number = "+123404"
        provider.language = "EN"
        provider.currency = "EUR"
        provider.save()
        self.provider = provider

    def teardown_method(self, test_method):
        ...

    def test_create_service_area_with_valid_polygon(self):
        client = APIClient()
        response = client.post(
            "/api/providers/" + str(self.provider.id) + "/serviceareas/",
            dict(
                provider=self.provider.id,
                name="service area",
                price=100,
                geojson="POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))"
            ),
        )
        print(response.data)
        assert response.status_code == status.HTTP_201_CREATED
    
    def test_create_service_area_with_invalid_polygon(self):
        client = APIClient()
        response = client.post(
            "/api/providers/" + str(self.provider.id) + "/serviceareas/",
            dict(
                provider=self.provider.id,
                name="service area",
                price=100,
                geojson="POLYGON ((0 0, 40 40, 0 40, 40 0, 0 15))"
            ),
        )
        print(response.data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
