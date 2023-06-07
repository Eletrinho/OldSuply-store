from django.contrib import admin
from .models import Product, Address, User

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'slug')
    class meta:
        model = Product

        
admin.site.register(User)
admin.site.register(Product, ProductAdmin)
admin.site.register(Address)
