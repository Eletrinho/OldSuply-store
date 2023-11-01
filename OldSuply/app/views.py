from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.contrib.auth import login, logout
from django.views.generic import DetailView, ListView
from django.contrib.auth.hashers import check_password

from .forms import UserForm
from .models import User, Product, Address
from pedidos.models import Pedidos
from cart.models import Carrinho
# Create your views here.

# index antigo
# def index(request):
#     first = Product.objects.first()
#     products = Product.objects.all()[1:4]
#     return render(request, 'index.html', {'products': products, 'first': first})

# index 2
def index(request):
    cart_obj, new_obj = Carrinho.objects.new_or_get(request)
    products = Product.objects.all()
    return render(request, 'index2.html', {'products': products, 'cart': cart_obj})

def novidades(request):
    return render(request, 'novidades.html')

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

#Class Based View
# class ProductListView(ListView):
#     #traz todos os produtos do banco de dados sem filtrar nada 
#     queryset = Product.objects.all()
#     template_name = "products.html"     
#     def get_context_data(self, *args, **kwargs):
#         context = super(ProductListView, self).get_context_data(*args, **kwargs)
#         print(context)
#         return context
    
def products_view(request):
    products = Product.objects.all()
    # print(request.session.get('cart_id'))
    return render(request, 'products.html', {'products': products})

class ProductDetailSlugView(DetailView):
    queryset = Product.objects.all()
    template_name = "detail.html"
    
    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailSlugView,  self).get_context_data(*args, **kwargs)
        # print(self.request.session.get('cart_id'))
        cart_obj, new_obj = Carrinho.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        try:
            instance = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            raise Http404("Não encontrado!")
        except Product.MultipleObjectsReturned:
            instance = Product.objects.filter(slug=slug).first()
        return instance

def profile_view(request, username):

    user_info = User.objects.filter(username=username).first()
    orders = Pedidos.objects.filter(address=Address.objects.filter(address_id=request.user).first())
    # ta dando erro isso, preciso colocar atributo 'owner' em pedidos type: ManyToMany
    return render(request, 'profile.html', {'user': user_info, 'orders': orders})
