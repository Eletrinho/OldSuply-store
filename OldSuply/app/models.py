from django.db import models
from django.utils import timezone
from django.core.mail import send_mail
from django.db.models.signals import pre_save
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

from .utils import unique_slug_generator

class UserManager(BaseUserManager):
    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not username:
            raise ValueError(_('The given username must be set'))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, is_staff=is_staff, is_active=True, is_superuser=is_superuser, last_login=now, date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        user=self._create_user(username, email, password, True, True, **extra_fields)
        user.is_active=True
        user.save(using=self._db)
        return user
                               
class User(AbstractBaseUser, PermissionsMixin): #define tabela Cliente

    #define nome das colunas e os tipos

    user_id = models.BigAutoField(primary_key=True, null=False)
    name = models.CharField(max_length=64, null=False)
    username = models.CharField(max_length=32, unique=True, null=False, error_messages={'unique': 'Esse username já foi registrado.'})
    email = models.EmailField(_('email address'), max_length=128, unique=True, null=False, error_messages={'unique': 'Esse email já foi registrado.'})
    phone = models.CharField(max_length=16)
    
    is_staff = models.BooleanField(_('staff status'), default=False,help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=True, help_text=_('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_trusty = models.BooleanField(_('trusty'), default=False, help_text=_('Designates whether this user has confirmed his account.'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name', ]

    objects = UserManager()
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    #puxa info, isso aqui n usa, tava só testando
    def all_info(self):
        return {'name': self.name,
                'username': self.username,
                'email': self.email,
                'password': self.password}
    
    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])
    
    def save(self, *args, **kwargs):
        if self.is_staff:
            super(User, self).save(*args, **kwargs)
        else:
            self.password = make_password(self.password, hasher='md5')
            super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.username


class Address(models.Model): #define tabela Endereço

    #ForeignKey com o user_id
    address_id = models.ForeignKey(User, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=128, null=False)
    city = models.CharField(max_length=64, null=False)
    state = models.CharField(max_length=64, null=False)
    cep = models.CharField(max_length=16, null=False)

    def __str__(self):
        return self.address_id.name


class Product(models.Model): #define tabela Produto

    product_id = models.BigAutoField(primary_key=True, null=False)
    name =  models.CharField(max_length=64, null=False)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(default=0.00, max_digits=65, decimal_places=2)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    stock = models.PositiveSmallIntegerField(null=False)
    sale = models.BooleanField()

    def get_absolute_url(self):
        return f"/products/{self.slug}/"
    
    def __str__(self):
        return self.name


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver, sender = Product)