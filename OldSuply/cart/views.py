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
