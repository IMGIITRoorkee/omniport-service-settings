from django.urls import path, include
from rest_framework import routers

from settings.views.biological_information import BiologicalInformationView
from settings.views.change_password import ChangePasswordView
from settings.views.change_secrets import ChangeSecretsView
from settings.views.display_picture import DisplayPictureView
from settings.views.financial_information import FinancialInformationView
from settings.views.political_information import PoliticalInformationView
from settings.views.residential_information import ResidentialInformationView
from settings.views.session_map import SessionMapViewSet

app_name = 'settings'

router = routers.SimpleRouter()
router.register('session_map', SessionMapViewSet, base_name='session_map')

urlpatterns = [
    path(
        'change_password/',
        ChangePasswordView.as_view(),
        name='change_password'
    ),
    path(
        'change_secrets/',
        ChangeSecretsView.as_view(),
        name='change_secrets'
    ),

    path(
        'display_picture/',
        DisplayPictureView.as_view(),
        name='display_picture'
    ),

    path(
        'biological_information/',
        BiologicalInformationView.as_view(),
        name='biological_information'
    ),
    path(
        'financial_information/',
        FinancialInformationView.as_view(),
        name='financial_information'
    ),
    path(
        'political_information/',
        PoliticalInformationView.as_view(),
        name='political_information'
    ),
    path(
        'residential_information/',
        ResidentialInformationView.as_view(),
        name='residential_information'
    ),

    path('', include(router.urls)),
]
