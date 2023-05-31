from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout as django_logout, get_user_model
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
    usuarioLogado = request.user
    
    if usuarioLogado.is_superuser:
        userModel = get_user_model()
        lista_usuarios = userModel.objects.all()
        dados = {
            'lista_produtos' : lista_produtos,
            'lista_usuarios': lista_usuarios,
        }
    elif usuarioLogado.is_staff:
        dados = {
            'lista_produtos' : lista_produtos,
        }
    elif usuarioLogado.is_active:
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

# View de login de usuário
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

# View de registro de usuário
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            password_confirmation = form.cleaned_data.get('password2')
            if User.objects.filter(username=username).exists():
                form.add_error('username', 'Username already exists.')
            elif password != password_confirmation:
                form.add_error('password2', 'Passwords do not match.')
            else:
                user = form.save(commit=False)
                user.set_password(password)
                user.save()
                login(request, user)  # LOGA O USUÁRIO APÓS O CADASTRO
                return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'home/register.html', {'form': form})
