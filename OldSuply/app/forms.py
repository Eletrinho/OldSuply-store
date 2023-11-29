from django import forms
from .models import User, Address

class UserForm(forms.ModelForm):
    name = forms.CharField(label="Nome completo:")
    email = forms.EmailField(label='Email:')
    username = forms.CharField(label='Nome de usuário:')
    phone = forms.CharField(label='Telefone:')
    password = forms.CharField(label='Senha:', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["name", "username", "email", "phone", "password"]

class AddressForm(forms.ModelForm):
    street_address = forms.CharField(label='Logradouro:')
    number = forms.CharField(label='Número:')
    bairro = forms.CharField(label='Bairro:')
    city = forms.CharField(label='Cidade:')
    state = forms.CharField(label='Estado:')
    cep = forms.CharField(label='CEP:')
    
    class Meta:
        model = Address
        fields = ["street_address", "number", "bairro", "city", "state", "cep"]
    
    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control mb-2'