from django.urls import path
from .views import prof_add, prof_view, review_add

app_name = 'prof'

urlpatterns = [
	path('adauga/', prof_add, name='prof_add'),
    path('id/<prof_id>/', prof_view, name='prof_view'),
    path('id/<prof_id>/adauga-nota', review_add, name='review_add'),
]