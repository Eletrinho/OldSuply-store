from django.shortcuts import render
from .models import Carrinho

def cart_home(request):
    cart_obj, new_obj = Carrinho.objects.new_or_get(request)
    return render(request, "home.html", {})