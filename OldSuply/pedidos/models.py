import math

from django.db import models
from django.db.models.signals import pre_save, post_save

from app.models import Address
from cart.models import Carrinho
from app.utils import unique_order_id_generator
# Create your models here.

ORDER_STATUS = (
    ('created', 'Criado'),
    ('paid', 'Pago'),
    ('shipped', 'Enviado'),
    ('refunded', 'Devolvido'),
)

class Pedidos(models.Model):

    order_id = models.CharField(max_length=128, blank=True)
    order_status = models.CharField(max_length=64, default='created', choices=ORDER_STATUS)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, blank=True)
    cart = models.ForeignKey(Carrinho, on_delete=models.CASCADE, null=True, blank=True)
    preco_prazo = models.DecimalField(default=10.99, max_digits=64, decimal_places=2)
    total = models.DecimalField(default=0, max_digits=64, decimal_places=2)

    def update_total(self):
        total, preco = self.cart.total, self.preco_prazo
        self.total = format(math.fsum([total, preco]))
        # self.total = total + preco
        self.save()
        return self.total
    
    def __str__(self):
        return self.order_id

def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)

pre_save.connect(pre_save_create_order_id, sender=Pedidos)

def post_save_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart_obj = instance
        cart_total = cart_obj.total
        cart_id = cart_obj.id
        qs = Pedidos.objects.filter(cart__id=cart_id)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()

post_save.connect(post_save_cart_total, sender=Carrinho)

def post_save_order(sender, instance, created, *args, **kwargs):
    print("Executando")
    if created:
        print("Atualizando")
        instance.update_total()

post_save.connect(post_save_order, sender=Pedidos)