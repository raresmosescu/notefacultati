from django.urls import path
from .views import school_view, school_add, school_ranking

app_name = 'school'

urlpatterns = [
    path('id/<school_id>', school_view, name='school_view'),
    path('adauga/', school_add, name='school_add'),
    path('clasament/', school_ranking, name='school_ranking')
]