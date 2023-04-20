from django.urls import path
from app_mercado import views

urlpatterns = [
    path('', views.index, name='index'),
]