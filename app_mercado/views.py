from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Produto

def index(request):
    lista_produtos = Produto.objects.all()
    template = loader.get_template('home/index.html')
    print(lista_produtos)
    context = {
        'lista_produtos' : lista_produtos,
    }
    return HttpResponse(template.render(context, request))