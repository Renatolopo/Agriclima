from django.urls import path
from .views import index, get_estacoes

urlpatterns = [
    path('', index, name='index'),
    path('get_estacoes/', get_estacoes, name='get_estacoes'),
]