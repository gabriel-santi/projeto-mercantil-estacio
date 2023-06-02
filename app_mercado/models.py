import uuid
from django.contrib.auth.models import User
from django.db import models

class Produto(models.Model):
    prod_desc = models.CharField(max_length=200)
    data_reg = models.DateTimeField('data registro')
    valor = models.DecimalField(decimal_places=2, max_digits=5)
    quantidade = models.IntegerField(default=1)

    def obterValorFormatado(self):
        return str(self.valor).replace(".",",")

    def __str__(self):
        return str(self.prod_desc)
    
class Carrinho(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    finalizado = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.id)
    
    @property
    def preco_total(self):
        itensCarrinho = self.itensCarrinho.all()
        total = sum([item.preco for item in itensCarrinho])
        return total
    
    @property
    def num_de_itens(self):
        itensCarrinho = self.itensCarrinho.all()
        quantidade = sum([item.quantidade for item in itensCarrinho])
        return quantidade
    
class ItemCarrinho(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='itens')
    carrinho = models.ForeignKey(Carrinho, on_delete= models.CASCADE, related_name="itensCarrinho")
    quantidade = models.IntegerField(default=0)
    
    def __str__(self):
        return self.produto.prod_desc
    
    @property
    def preco(self):
        novoPreco = self.produto.valor * self.quantidade
        return novoPreco
    
    @property
    def preco_unitario(self):
        novoPreco = self.produto.valor
        return novoPreco
    
    @property
    def get_id(self):
        return self.produto.id