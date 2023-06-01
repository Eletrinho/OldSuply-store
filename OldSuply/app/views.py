from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password
from .forms import UserForm
from .models import User, Product
# Create your views here.

def index(request):
    # if request.user.is_authenticated:
    #     logged = True
    return render(request, 'index.html')

def registrar(request):
    form = UserForm()
    if request.method == 'POST':
        new_user = UserForm(request.POST)
        if new_user.is_valid():
            new_user.save()
            return HttpResponseRedirect("/")
        else:
            return render(request, 'register.html', {"form": form, 'error': new_user.errors})
    else:
        return render(request, 'register.html', {"form": form})

def logar(request):
    if request.method == 'POST':
        username = request.POST['username']
        user = User.objects.filter(username=username).first()
        password = request.POST['password']
        if not user == None and check_password(password, user.password):
            login(request, user)
            return HttpResponseRedirect("/")
        else:
            return render(request, "login.html", {'error': 'dados inválidos'})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")

def products_view(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})