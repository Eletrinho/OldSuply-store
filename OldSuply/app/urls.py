from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'app'
urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.registrar, name='registrar'),
    path('login', views.logar, name='logar'),
    path('logout', views.logout_view, name='lougout'),
    path('products', views.products_view, name='produtos')
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)