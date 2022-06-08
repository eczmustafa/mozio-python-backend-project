from django.urls import path
from django.urls.conf import include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('providers', views.ProviderViewSet, basename='providers')

service_areas_router = routers.NestedDefaultRouter(
    router, 'providers', lookup='provider')
service_areas_router.register('serviceareas', views.ServiceAreaViewSet,
                         basename='service-areas')

# URLConf
urlpatterns = [
    path("search/",views.QueryServiceAreas.as_view())
]

urlpatterns += router.urls + service_areas_router.urls
