from django.urls import path
from .views import search, ajax_school, results, school_profs

app_name = 'search'

urlpatterns = [
    path('', search, name='search'),
    path('ajax_school/', ajax_school, name='ajax_school'),
    path('rezultate/', results, name='results'),
    path('facultate/<id_facultate>/', school_profs, name='school_profs'),
]