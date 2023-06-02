from datetime import date
import datetime
import json
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout as django_logout, get_user_model
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from .models import Produto, Carrinho, ItemCarrinho
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def index(request):
    lista_produtos = Produto.objects.order_by("data_reg")
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
        carrinho, created = Carrinho.objects.get_or_create(usuario=request.user, finalizado=False)
        paginator = Paginator(lista_produtos, 12)
        page = request.GET.get('pagina')
        lista_paginada = paginator.get_page(page)
        dados = {
            'lista_produtos' : lista_paginada,
            'carrinho': carrinho
        }

    template = loader.get_template('home/index.html')
    return HttpResponse(template.render(dados, request))

@login_required(login_url='/login/')
def cadastrar_produto(request):
    template = loader.get_template('home/cadastro-produto.html')

    if request.method == "POST":
        desc = request.POST.get('descricao')
        valor = request.POST.get('valor')
        qtd =  request.POST.get('quantidade')
        data = datetime.datetime.now()

        if desc and valor and qtd:
            Produto.objects.create(prod_desc=desc, valor=valor, quantidade=qtd, data_reg=data)
            return redirect('index')
        else:
            return HttpResponse(template.render({'erro': '*Preencha todos os campos'}, request))
    else:
        return HttpResponse(template.render({}, request))

@login_required(login_url='/login/')
def editar_produto(request, id):
    produto = Produto.objects.get(id=id)
    template = loader.get_template('home/editar-produto.html')

    if request.method == 'POST':
        id = request.POST.get('prod_id')
        desc = request.POST.get('descricao')
        valor = request.POST.get('valor')
        qtd =  request.POST.get('quantidade')
        if desc and valor and qtd:
            produtoEditado = Produto(id=id, prod_desc=desc, valor=valor, quantidade=qtd, data_reg=produto.data_reg)
            produtoEditado.save()
            return redirect('index')
        else:
            return HttpResponse(template.render({'produto':produto, 'erro': '*Preencha todos os campos'}, request))
    else:
        return HttpResponse(template.render({'produto':produto}, request))

@login_required(login_url='/login/')
def deletar_produto(request, id):
    produto = Produto.objects.get(id=id)
    produto.delete()
    return redirect('index')

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

@login_required(login_url='/login/')
def cadastrar_usuario(request):
    if request.method == 'POST':
        checkbox = request.POST.get('funcionario')
        is_staff = checkbox == 'on'

        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            password_confirmation = form.cleaned_data.get('password2')

            if User.objects.filter(username=username).exists():
                form.add_error('username', 'Já existe um usuário com esse nome.')
                return render(request, 'home/cadastro-usuario.html', {'form': form})

            elif password != password_confirmation:
                form.add_error('password2', 'Senhas não coincidem.')
                return render(request, 'home/cadastro-usuario.html', {'form': form})

            user = User.objects.create_user(username=username, password=password, is_staff=is_staff)
            user.save()

            return redirect('index')       
    else:
        form = UserCreationForm()
    return render(request, 'home/cadastro-usuario.html', {'form': form})    

@login_required(login_url='/login/')
def deletar_usuario(request, id):
    usuarioLogado = request.user

    if usuarioLogado.is_superuser and usuarioLogado.id != id:
        usuario = User.objects.get(id=id)
        usuario.delete()

    return redirect('index', {'error': 'Não é possível excluir o próprio usuário'})

@login_required(login_url='/login/')
def carrinho(request):
    if request.method == 'GET':
        carrinho = None
        itensCarrinho = []
    
        if request.user.is_authenticated:
            carrinho, created = Carrinho.objects.get_or_create(usuario=request.user, finalizado=False)
            itensCarrinho = carrinho.itensCarrinho.all()
        
        context = {"carrinho":carrinho, "itens_carrinho":itensCarrinho}
        template = loader.get_template('home/carrinho.html')
        return HttpResponse(template.render(context, request))

@login_required(login_url='/login/')
def carrinho_adicionar(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id_produto = data["id"]
        produto = Produto.objects.get(id=id_produto)

        if produto.quantidade>0:
            carrinho, created = Carrinho.objects.get_or_create(usuario=request.user, finalizado=False)
            itemCarrinho, created = ItemCarrinho.objects.get_or_create(carrinho=carrinho, produto=produto)
            if produto.quantidade > itemCarrinho.quantidade:
                itemCarrinho.quantidade += 1
                itemCarrinho.save()
            
        num_de_itens = carrinho.num_de_itens
        
        return JsonResponse(num_de_itens, safe=False)
        
@login_required(login_url='/login/')
def carrinho_remover(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id_produto = data["id"]
        produto = Produto.objects.get(id=id_produto)

        carrinho, created = Carrinho.objects.get_or_create(usuario=request.user, finalizado=False)
        itemCarrinho, created = ItemCarrinho.objects.get_or_create(carrinho=carrinho, produto=produto)
        if itemCarrinho.quantidade > 1:
            itemCarrinho.quantidade -= 1
            itemCarrinho.save()
        else:
            itemCarrinho.delete()
        
        num_de_itens = carrinho.num_de_itens
        
        return JsonResponse(num_de_itens, safe=False)
    
@login_required(login_url='/login/')
def carrinho_finalizar(request, pk):
    carrinho = Carrinho.objects.get(id=pk)
    itensCarrinho = carrinho.itensCarrinho.all()

    for item in itensCarrinho:
        produto = Produto.objects.get(id=item.get_id)
        produto.quantidade = produto.quantidade - item.quantidade
        produto.save() 

    carrinho.finalizado = True
    carrinho.save()
    return redirect("index")