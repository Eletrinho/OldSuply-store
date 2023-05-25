from django.urls import path
from . import views

app_name = 'app'
urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.registrar, name='registrar'),
    path('login', views.logar, name='logar'),
    path('logout', views.logout_view, name='lougout')
]