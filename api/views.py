from django.shortcuts import render
from django.contrib.gis.geos import Point
from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import status, generics
from .models import Provider,ServiceArea
from .serializers import ProviderSerializer, ServiceAreaSerializer, ServiceAreaSearchSerializer
from django.core.exceptions import BadRequest


class ProviderViewSet(ModelViewSet):
    """
    Returns a list of all providers in the system.

    Allows CRUD operations.

    **Authentication is not implemented.** However, each provider has a UUID.

    GET request of */api/providers/[uuid]]/* and */api/providers/[uuid]]/serviceareas*
    retrieves the provider details and service areas respectively.
    So, other providers cannot see or modify the others' data.
    """
    queryset = Provider.objects.prefetch_related("serviceareas").all()
    serializer_class = ProviderSerializer

    def destroy(self, request, *args, **kwargs):
        if ServiceArea.objects.filter(provider_id=kwargs['pk']):
            return Response({'error': 'Provider cannot be deleted because it is related one or more service areas.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return super().destroy(request, *args, **kwargs)


class ServiceAreaViewSet(ModelViewSet):
    """
    Returns a list of all service areas of the provider with the UUID.

    Allows CRUD operations.
    """
    #queryset = ServiceArea.objects.select_related("provider").all()
    serializer_class = ServiceAreaSerializer
    
    def get_serializer_context(self):
        return {'request': self.request}
    
    def get_queryset(self):
        return ServiceArea.objects \
            .filter(provider_id=self.kwargs['provider_pk']) \
            .select_related('provider')


class QueryServiceAreas(generics.ListAPIView):
    """
    Returns the list of service areas with the given point.
    
    Example of a query: */api/search/?latitude=25&longitude=15*
    """
    serializer_class = ServiceAreaSearchSerializer

    def get_queryset(self):
        latitude=self.request.query_params.get("latitude")
        longitude=self.request.query_params.get("longitude")
        try:
            latitude=float(latitude)
            longitude=float(longitude)
        except Exception as ex:
            raise BadRequest("Invalid parameters")
            
        query_point = Point(latitude, longitude)

        return ServiceArea.objects.filter(geojson__contains=query_point).select_related("provider")
