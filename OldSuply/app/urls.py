from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'app'
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.registrar, name='registrar'),
    path('login/', views.logar, name='logar'),
    path('logout/', views.logout_view, name='lougout'),
    path('profile/<username>', views.profile_view, name='profile'),
    path('products/', views.products_view, name='produtos'),
    # path('products/', views.ProductListView.as_view()),
    path('products/<slug:slug>/', views.ProductDetailSlugView.as_view())
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)