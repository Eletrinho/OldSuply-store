from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .forms import UserForm
from .models import User
# Create your views here.

def index(request):
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
        m = User.objects.get(username=request.POST["username"])
        
    return render(request, 'login.html')

def logout(request):
    try:
        del request.session["user_id"]
    except KeyError:
        pass
    return HttpResponse("You're logged out.")