import os
import json
import requests

from dotenv import load_dotenv, find_dotenv

from .models import Carrinho
from app.models import Product, Address
from pedidos.models import Pedidos
from django.shortcuts import render, redirect

def cart_home(request):
    cart_obj, new_obj = Carrinho.objects.new_or_get(request)
    products = cart_obj.products.all()
    logged = False
    if request.user.is_authenticated:
        logged = True
    return render(request, "cart.html", {"cart": cart_obj, "products": products, 'logged': logged})

def cart_update(request):
    print(request.POST)
    product_id = request.POST.get('product_id')
    if product_id is not None:
        try:
            product_obj = Product.objects.get(product_id=product_id)
        except Product.DoesNotExist:
            print("Mostrar mensagem ao usuário, esse produto acabou!")
            return redirect("cart:home")

    cart_obj, new_obj = Carrinho.objects.new_or_get(request)
    if product_obj in cart_obj.products.all():
        cart_obj.products.remove(product_obj)
    else:
        cart_obj.products.add(product_obj)
    return redirect("cart:home")

def checkout_home(request):
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
    
    return render(request, "checkout1.html", {"object": order_obj, 'fretes': resposta})

def calc_frete(request):

    cart_obj, cart_created = Carrinho.objects.new_or_get(request)
    order_obj = None

    if cart_created or cart_obj.products.count() == 0:
        return redirect("cart:home")

    else:
        order_obj, new_order_obj = Pedidos.objects.get_or_create(cart=cart_obj)

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
    # for i in resposta:
    #     print(i['picture'])

    return render(request, 'frete.html', {'fretes': resposta})