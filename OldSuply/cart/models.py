from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save, m2m_changed
from app.models import Product

User = settings.AUTH_USER_MODEL
class CarrinhoManager(models.Manager):
    def new_or_get(self, request):
        cart_id = request.session.get("cart_id", None)
        qs = Carrinho.objects.filter(id=cart_id)
        if len(qs) == 1:
            new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = Carrinho.objects.new(user=request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id
            print(f'depois: {request.session.get("cart_id")}')
        return cart_obj, new_obj
    
    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)

class Carrinho(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    products = models.ManyToManyField(Product, blank= True)
    total = models.DecimalField(default=0.00, max_digits=65, decimal_places=2)
    # subtotal = models.DecimalField(default=0.00, max_digits=65, decimal_places=2)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CarrinhoManager()

    def __str__(self):
        return str(self.id)

def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
  if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
    products = instance.products.all() 
    total = 0 
    for product in products: 
      total += product.price 
    # if instance.subtotal != total:
    #   instance.subtotal = total
    #   instance.save()
    # instance.subtotal = total
    instance.save()

m2m_changed.connect(m2m_changed_cart_receiver, sender = Carrinho.products.through)

# def pre_save_cart_receiver(sender, instance, *args, **kwargs):
#     if instance.subtotal > 0:
#         instance.total = instance.subtotal  + 10 # considere o 10 como uma taxa de entrega
#     else:
#         instance.total = 0.00

# pre_save.connect(pre_save_cart_receiver, sender = Carrinho)