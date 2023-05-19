from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.core.paginator import Paginator
from .forms import MyForm

from .models import Produto

def index(request):
    lista_produtos = Produto.objects.all()

    paginator = Paginator(lista_produtos, 12)
    page = request.GET.get('pagina')
    lista_paginada = paginator.get_page(page)

    dados = {
        'lista_produtos' : lista_paginada,
    }

    template = loader.get_template('home/index.html')

    return HttpResponse(template.render(dados, request))

def cadastrar(request):
    template = loader.get_template('home/cadastro.html')

    if request.method == "POST":
        form = MyForm(request.POST)
        if form.is_valid():
            form.data.values
            print(form.fields['data_reg'].value)
            #form.save()
    else:
        form = MyForm()

    return HttpResponse(template.render({'form': form}, request))