from django.contrib import admin
from . import models

# Register your models here.
class CarrinhoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'total')
    class meta:
        model = models.Carrinho

admin.site.register(models.Carrinho, CarrinhoAdmin)