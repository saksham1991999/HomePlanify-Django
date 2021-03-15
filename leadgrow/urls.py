from django.urls import path, include
from rest_framework.routers import DefaultRouter

from leadgrow.views import BusinessAPIViewSet, CustomerAPIViewSet, LabelAPIViewSet, TaskAPIViewSet, NoteAPIViewSet


app_name = 'leadgrow'


router = DefaultRouter()
router.register('business', BusinessAPIViewSet, basename='business')
router.register('customer', CustomerAPIViewSet, basename='customer')
router.register('labels', LabelAPIViewSet, basename='label')
router.register('tasks', TaskAPIViewSet, basename='task')
router.register('notes', NoteAPIViewSet, basename='note')

urlpatterns = [
    path('', include(router.urls)),
]