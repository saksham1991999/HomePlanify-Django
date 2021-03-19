from django.urls import path, include
from rest_framework.routers import DefaultRouter

from feawa.views import ZoneAPIViewSet, FirmAPIViewSet


app_name = 'feawa'


router = DefaultRouter()
router.register('zones', ZoneAPIViewSet, basename='zone')
router.register('firms', FirmAPIViewSet, basename='firm')

urlpatterns = [
    path('', include(router.urls)),
]