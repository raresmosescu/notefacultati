from django.urls import path
from .views import user_create, login_view, logout_view, user_profile, user_activate

app_name = 'user'

urlpatterns = [
    path('creaza-cont/', user_create, name='user_create'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'), 
    path('profil/', user_profile, name='user_profile'),
    path('activate/', user_activate, name='user_activate'),
]