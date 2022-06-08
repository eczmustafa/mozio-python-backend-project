import pytest
from api.models import Provider, ServiceArea
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestCreateProvider:
    def setup_method(self, test_method):
        provider = Provider()
        provider.name = "test provider"
        provider.email = "test@provider.com"
        provider.phone_number = "+123404"
        provider.language = "EN"
        provider.currency = "EUR"
        provider.save()

        self.provider = provider

    def teardown_method(self, test_method):
        ...

    def test_create_provider_with_an_already_existing_email(self):
        client = APIClient()
        response = client.post(
            "/api/providers/",
            dict(
                name="another test provider with same name",
                email="test@provider.com",
                phone_number="+0000",
                language="EN",
                currency="EUR",
            ),
        )
        print(response.data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
