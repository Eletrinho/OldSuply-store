import requests
from .models import Pedidos
from cart.models import Carrinho
from django.shortcuts import render

# Create your views here.

#fazer um blg q quando finaliza o pedido tira 1 do 'stock' no produto

def gerar_qr(request):
    cart_obj, cart_created = Carrinho.objects.new_or_get(request)
    order_obj, new_order_obj = Pedidos.objects.get_or_create(cart=cart_obj)

    # preco = order_obj.total * 100
    # preco = str(preco)
    preco = str(order_obj.total)
    preco = preco.replace('.', '')
    print(preco)
    url = "https://sandbox.api.pagseguro.com/orders"

    payload = {
        "customer": {
            "tax_id": "12345678909",
            "email": f"{cart_obj.user.email}",
            "name": f"{cart_obj.user.name}"
        },
        "reference_id": f"{order_obj.order_id}",
        "qr_codes": [{ "amount": { "value": f'{preco}' } }]
    }
    headers = {
        "accept": "application/json",
        "Authorization": "0DBA84D4CDE844E0B23CD2FFF403E32F",
        "content-type": "application/json"
    }

    # usando o modo sandbox até vai, mas precisa de permissão deleas pra deixar o trem em produção
    # tenta criar conta no mercado pago
    response = requests.post(url, json=payload, headers=headers)

    print(response.text)

    return render(request, "checkout.html", {"object": order_obj})