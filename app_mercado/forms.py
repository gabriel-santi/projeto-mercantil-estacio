
from django import forms
from .models import Produto
    
class MyForm(forms.ModelForm):
  class Meta:
    model = Produto
    fields = ["prod_desc", "valor", "quantidade", "data_reg"]
    labels = {"prod_desc": "Descrição", "valor": "Preço unitário", "quantidade": "Quantidade"}