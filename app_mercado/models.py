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