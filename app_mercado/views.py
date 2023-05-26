from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout as django_logout
from django.http import HttpResponse
from django.template import loader
from django.core.paginator import Paginator
from .forms import MyForm
from django.contrib.auth.models import User
from .models import Produto
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
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

def login_view(request):
    if request.method == "GET":
        return render(request, 'home/login.html', {'form': AuthenticationForm()})
    else:
        usuario = request.POST.get('usuario')
        senha = request.POST.get('senha')
        usuario = authenticate(request, username=usuario, password=senha)

        if usuario is not None:
            login(request, usuario)
            return redirect('index')
        else:
            return render(request, 'home/login.html', {'form': AuthenticationForm(), 'erro': 'Usuário/senha inválido'})

@login_required(login_url='/login/')
def logout(request):
    django_logout(request)
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['senha']
        user = authenticate(request, username=username, password=password)
    else:
        form = UserCreationForm()
        return render(request, 'home/register.html', {'form': form})
