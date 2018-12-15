from django.urls import path, include
from rest_framework import routers

from settings.views.session_map import SessionMapViewSet

app_name = 'settings'

router = routers.SimpleRouter()
router.register('session_map', SessionMapViewSet, base_name='session_map')

urlpatterns = [
    path('', include(router.urls)),
]
