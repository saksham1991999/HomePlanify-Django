from django.urls import path, include
from rest_framework.routers import DefaultRouter

from leadgrow.views import BusinessAPIViewSet, CustomerAPIViewSet, LabelAPIViewSet


app_name = 'leadgrow'


router = DefaultRouter()
router.register('business', BusinessAPIViewSet, basename='business')
router.register('customer', CustomerAPIViewSet, basename='customer')
router.register('labels', LabelAPIViewSet, basename='label')

urlpatterns = [
    path('', include(router.urls)),
]