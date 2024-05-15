from django.shortcuts import render
from django.http import JsonResponse
from .models import Estacao

# Create your views here.
def index(request):
    return render(request,'index.html')




def get_estacoes(request):
    estacoes = Estacao.objects.all().values('nome', 'codigo', 'latitude', 'longitude', 'tipoEstacao', 'fonte')
    # estacoes = Estacao.objects.all()
    # print(estacoes)
    return JsonResponse(list(estacoes), safe=False)












# def get_nome_estacao(request):
#     # Obtém as coordenadas da solicitação
#     latitude = float(request.GET.get('latitude'))
#     longitude = float(request.GET.get('longitude'))
    
#     # Consulta ao banco de dados para encontrar a estação mais próxima das coordenadas clicadas
#     estacao = Estacao.objects.filter(latitude=latitude, longitude=longitude).first()
    
#     # Verifica se uma estação foi encontrada
#     if estacao:
#         # Retorna o nome da estação como resposta JSON
#         return JsonResponse({'nomeEstacao': estacao.nome})
#     else:
#         # Se nenhuma estação for encontrada, retorna uma resposta vazia
#         return JsonResponse({}, status=404)