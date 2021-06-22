from django.urls import path, re_path
from .views import school_view, school_add

app_name = 'school'

urlpatterns = [
    path('id/<school_id>', school_view, name='school_view'),
    path('adauga/', school_add, name='school_add'),
]