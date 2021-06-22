from django.urls import path
from .views import ajax_cities, ajax_departments

app_name = 'site_utility'

urlpatterns = [
    path('ajax_cities/', ajax_cities, name='ajax_cities'),
    path('ajax_departments/', ajax_departments, name='ajax_departments'),
]