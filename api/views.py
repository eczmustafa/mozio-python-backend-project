from django.contrib.gis.geos import Point
from django.core.exceptions import BadRequest
from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404, render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Provider, ServiceArea
from .serializers import (
    ProviderSerializer,
    ServiceAreaSearchSerializer,
    ServiceAreaSerializer,
)


class ProviderViewSet(ModelViewSet):
    """
    Returns a list of all providers in the system.

    Allows CRUD operations.

    **Authentication is not implemented.** However, each provider has a UUID.

    GET request of */api/providers/[uuid]/* and */api/providers/[uuid]/serviceareas*
    retrieve the provider details and service areas respectively.
    So, other providers cannot see or modify the others' data.
    """

    queryset = Provider.objects.prefetch_related("serviceareas").all()
    serializer_class = ProviderSerializer

    def destroy(self, request, *args, **kwargs):
        if ServiceArea.objects.filter(provider_id=kwargs["pk"]):
            return Response(
                {
                    "error": "Provider cannot be deleted because it is related one or more service areas."
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )

        return super().destroy(request, *args, **kwargs)


class ServiceAreaViewSet(ModelViewSet):
    """
    Returns a list of all service areas of the provider with the UUID.
    
    CRUD operations can be carried out through this end point:
    */api/providers/[uuid]/serviceareas/[id]/*

    Sample polygon input for Geojson field: POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))
    """

    # queryset = ServiceArea.objects.select_related("provider").all()
    serializer_class = ServiceAreaSerializer

    def get_serializer_context(self):
        return {"request": self.request, "provider_id": self.kwargs["provider_pk"]}

    def get_queryset(self):
        return ServiceArea.objects.filter(
            provider_id=self.kwargs["provider_pk"]
        ).select_related("provider")


class QueryServiceAreas(generics.ListAPIView):
    """
    Returns the list of service areas with the given point.

    Example of a query: */api/search/?latitude=25&longitude=15*
    """

    serializer_class = ServiceAreaSearchSerializer

    def get_queryset(self):
        latitude = self.request.query_params.get("latitude")
        longitude = self.request.query_params.get("longitude")
        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except Exception as ex:
            raise BadRequest(
                "Invalid parameters. Sample usage: /api/search/?latitude=25&longitude=15"
            )

        query_point = Point(latitude, longitude)

        return ServiceArea.objects.filter(geojson__contains=query_point).select_related(
            "provider"
        )


class DocsView(APIView):
    """
    CRUD operations for providers and service areas.

    **List of providers:**
    *providers/*

    **Details of providers:**
    *providers/[uuid]*

    **Service area of a provider:**
    *providers/[uuid]/serviceareas*

    **Details of a service area:**
    *providers/[uuid]/serviceareas/[id]*




    """

    def get(self, request, *args, **kwargs):
        apidocs = {
            "List of Providers": request.build_absolute_uri("providers/"),
            "Example Service Area Search": request.build_absolute_uri(
                "search/?latitude=25&longitude=15"
            ),
        }
        return Response(apidocs)
