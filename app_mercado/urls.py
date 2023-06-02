from django.urls import path
from app_mercado import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout, name='logout'),
    path('produto/cadastrar', views.cadastrar_produto, name='cadastrar-produto'),
    path('produto/editar/<int:id>', views.editar_produto, name='editar-produto'),
    path('produto/deletar/<int:id>', views.deletar_produto, name='deletar-produto'),
    path('usuario/cadastrar', views.cadastrar_usuario, name='cadastrar-usuario'),
    path('usuario/deletar/<int:id>', views.deletar_usuario, name='deletar-usuario'),
    path('carrinho/', views.carrinho, name='carrinho'),
    path('carrinho/adicionar', views.carrinho_adicionar, name='carrinho-adicionar'),    
    path('carrinho/remover', views.carrinho_remover, name='carrinho-remover'),
    path('carrinho/finalizar/<str:pk>', views.carrinho_finalizar, name='carrinho-finalizar'),
]