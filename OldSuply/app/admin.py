from django.contrib import admin
from .models import Product, Address, User

# Register your models here.
admin.site.register(User)
admin.site.register(Product)
admin.site.register(Address)
