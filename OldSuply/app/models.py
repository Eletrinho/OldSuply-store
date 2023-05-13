from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password

class Client(AbstractUser): #define tabela Cliente

    #define nome das colunas e os tipos

    user_id = models.BigAutoField(primary_key=True, null=False)
    name = models.CharField(max_length=64, null=False)
    username = models.CharField(max_length=32, unique=True, null=False, error_messages={'unique': 'Esse username já foi registrado.'})
    email = models.EmailField(max_length=128, unique=True, null=False, error_messages={'unique': 'Esse email já foi registrado.'})
    password = models.CharField(max_length=128, null=False)
    phone = models.CharField(max_length=16, unique=True, null=False, error_messages={'unique': 'Esse número já foi registrado.'})


    #criptografa a senha
    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super(Client, self).save(*args, **kwargs)

    #puxa info, isso aqui n usa, tava só testando
    def all_info(self):
        return {'name': self.first_name + ' ' + self.last_name,
                'username': self.username,
                'email': self.email,
                'password': self.password}

    def __str__(self):
        return self.username


class Address(models.Model): #define tabela Endereço

    #ForeignKey com o user_id
    address_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=128, null=False)
    city = models.CharField(max_length=64, null=False)
    state = models.CharField(max_length=64, null=False)
    cep = models.CharField(max_length=16, null=False)


class Product(models.Model): #define tabela Produto

    product_id = models.BigAutoField(primary_key=True, null=False)
    name =  models.CharField(max_length=64, null=False)
    price = models.FloatField(null=False)
    stock = models.PositiveSmallIntegerField(null=False)
    sale = models.BooleanField(null=False)