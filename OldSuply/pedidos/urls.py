from django.urls import path
from . import views

app_name = "checkout"

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('update/', views.checkout_update, name='update'),
    # path('pagamento/', views.gerar_qr, name='payment')
    path('pagamento/<order_id>', views.payment, name='payment')
]