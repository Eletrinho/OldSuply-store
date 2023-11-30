from django import forms
from .models import User, Address

class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nome de Usuário'}))
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nome Completo'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Telefone'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Senha'}))

    class Meta:
        model = User
        fields = ["name", "username", "email", "phone", "password"]
    
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control rounded-left'

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