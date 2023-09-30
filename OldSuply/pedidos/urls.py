from django.urls import path
from . import views

app_name = "checkout"

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('gerar/', views.gerar_qr, name='gerar_qr')
]