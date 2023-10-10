# Fazer o form input radio pra alterar o valor do carrinho + frete
from django import forms

class FreteForm(forms.Form):
    fretes_choice = forms.ChoiceField(widget=forms.RadioSelect)