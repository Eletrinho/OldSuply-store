from django.urls import path
from . import views

app_name = "check"

urlpatterns = [
    path('gerar/', views.gerar_qr, name='gerar_qr')
]