from .models import Carrinho
from app.models import Product, Address
from django.shortcuts import render, redirect

def cart_home(request):
    address = None
    if request.user.is_authenticated:
        address = Address.objects.filter(address_id=request.user).first()
    cart_obj, new_obj = Carrinho.objects.new_or_get(request)
    products = cart_obj.products.all()
    return render(request, "cart.html", {"cart": cart_obj, "products": products, 'address': address})

def cart_update(request):
    # print(request.POST)
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
    request.session['cart_items'] = cart_obj.products.count()
    return redirect("cart:home")
