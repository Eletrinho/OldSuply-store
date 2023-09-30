import requests
import os

from .models import Pedidos
from app.models import Address
from cart.models import Carrinho

from dotenv import load_dotenv, find_dotenv
from django.shortcuts import render, redirect
# Create your views here.

def checkout(request):
    cart_obj, cart_created = Carrinho.objects.new_or_get(request)
    order_obj = None

    if cart_created or cart_obj.products.count() == 0:
        return redirect("cart:home")
    else:
        order_obj, new_order_obj = Pedidos.objects.get_or_create(cart=cart_obj)
        order_obj.address = Address.objects.filter(address_id=request.user).first()
    
    cep_c = order_obj.address.cep

    load_dotenv(find_dotenv())
    url = "https://sandbox.superfrete.com/api/v0/calculator"

    payload = {
        "from": { "postal_code": "37600000" },
        "to": { "postal_code": f"{cep_c}" },
        "services": "1,2,17",
        "options": {
            "own_hand": False,
            "receipt": False,
            "insurance_value": 0,
            "use_insurance_value": False
        },
        "package": {
            "height": 2,
            "width": 11,
            "length": 16,
            "weight": 0.3
        }
    }
    headers = {
        "accept": "application/json",
        "User-Agent": "Nome e versão da aplicação (email para contato técnico)",
        "content-type": "application/json",
        "Authorization": f"Bearer {os.environ.get('FRETE_TOKEN')}"
        }


    response = requests.post(url, json=payload, headers=headers)
    resposta = response.json()
    
    return render(request, "checkout.html", {"object": order_obj, 'fretes': resposta})

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