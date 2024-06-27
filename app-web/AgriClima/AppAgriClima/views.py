from django.shortcuts import render
from django.http import JsonResponse
from .models import Estacao
from .utils import download_station_data, clear_output_directory
from django.http import HttpResponse, Http404
from django.conf import settings
import os

# Create your views here.
def index(request):
    return render(request,'index.html')




def get_estacoes(request):
    estacoes = Estacao.objects.exclude(tipoEstacao=1).values('nome', 'codigo', 'latitude', 'longitude', 'tipoEstacao', 'fonte')
    # estacoes = Estacao.objects.all()
    # print(estacoes)
    return JsonResponse(list(estacoes), safe=False)

def download_station_data_view(request):
    if request.method == 'POST':
        codigo_estacao = request.POST.get('cod-estacao')
        nome_estacao = request.POST.get('nome-estacao').replace(" ", "_")  # Replace spaces with underscores
        if codigo_estacao and nome_estacao:
            diretorio_saida = os.path.join(settings.MEDIA_ROOT, 'saida')
            
            # Limpar a pasta de saída antes de baixar o novo arquivo
            clear_output_directory(diretorio_saida)
            
            file_path = download_station_data(codigo_estacao, nome_estacao, diretorio_saida)
            if file_path:
                if "Nenhum arquivo CSV encontrado no ZIP" in file_path or "Cabeçalho 'EstacaoCodigo' não encontrado" in file_path:
                    return JsonResponse({'success': False, 'error': 'Está estação não contém dados'})
                else:
                    relative_path = os.path.relpath(file_path, settings.MEDIA_ROOT)
                    return JsonResponse({'success': True, 'file_path': settings.MEDIA_URL + relative_path, 'file_name': f"{nome_estacao}_{codigo_estacao}_data.csv"})
            else:
                return JsonResponse({'success': False, 'error': 'Failed to download file'})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid station code or name'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})



def serve_csv(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, 'saida', filename)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
    else:
        raise Http404









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