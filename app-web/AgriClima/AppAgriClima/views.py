from django.shortcuts import render
from django.http import JsonResponse
from .models import Estacao

# Create your views here.
def index(request):
    return render(request,'index.html')




def get_estacoes(request):
    estacoes = Estacao.objects.all().values('nome', 'latitude', 'longitude')
    return JsonResponse(list(estacoes), safe=False)