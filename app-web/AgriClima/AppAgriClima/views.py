from django.shortcuts import render
from django.http import JsonResponse
from .models import Estacao
from .utils import download_station_data_general, clear_output_directory, download_multiple_stations
from django.http import HttpResponse, Http404
from django.conf import settings
import os
from urllib.parse import unquote
import pandas as pd
import json
from django.views.decorators.csrf import csrf_exempt
import io
import zipfile
from datetime import datetime


def converter_data(data_aaaa_mm_dd):
    # Converte a string para um objeto datetime
    data = datetime.strptime(data_aaaa_mm_dd, '%Y-%m-%d')
    # Converte o objeto datetime para uma string no formato desejado
    data_formatada = data.strftime('%d/%m/%Y')
    return data_formatada


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
        data_inicio = converter_data(request.POST.get('start-date'))
        data_fim = converter_data(request.POST.get('end-date'))
        fonte = request.POST.get('fonte')

        
        print(f"Received POST request with parameters: codigo_estacao={codigo_estacao}, nome_estacao={nome_estacao}, fonte={fonte}, data_inicio={data_inicio}, data_fim={data_fim}")

        
        if codigo_estacao and nome_estacao and fonte:
            diretorio_saida = os.path.join(settings.MEDIA_ROOT, 'saida')
            
            # Limpar a pasta de saída antes de baixar o novo arquivo
            clear_output_directory(diretorio_saida)
            
            try:
                file_path = download_station_data_general(codigo_estacao, nome_estacao, diretorio_saida, fonte, data_inicio, data_fim)
                if file_path:
                    if "Nenhum arquivo CSV encontrado no ZIP" in file_path or "Cabeçalho 'EstacaoCodigo' não encontrado" in file_path:
                        return JsonResponse({'success': False, 'error': 'Está estação não contém dados'})
                    else:
                        relative_path = os.path.relpath(file_path, settings.MEDIA_ROOT)
                        return JsonResponse({'success': True, 'file_path': settings.MEDIA_URL + relative_path, 'file_name': os.path.basename(file_path)})
                else:
                    return JsonResponse({'success': False, 'error': 'Failed to download file'})
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid station code or name or fonte'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@csrf_exempt
def download_multiple_stations_data(request):
    if request.method == 'POST':
        stations = json.loads(request.body)
        diretorio_saida = os.path.join(settings.MEDIA_ROOT, 'saida')
        try:
            # Limpar a pasta de saída antes de baixar o novo arquivo
            clear_output_directory(diretorio_saida)
            
            results = []
            for station in stations:
                codigo_estacao = station['codigo']
                nome_estacao = station['nome'].replace(" ", "_")
                fonte = station['fonte']
                data_inicio = None
                data_fim = None
                if fonte == 'INMET':
                    data_inicio = converter_data(station['start-date'])
                    data_fim = converter_data(station['end-date'])
                    
                    
                print(f"Received POST request with parameters: codigo_estacao={codigo_estacao}, nome_estacao={nome_estacao}, fonte={fonte}, data_inicio={data_inicio}, data_fim={data_fim}")


                try:
                    file_path = download_station_data_general(codigo_estacao, nome_estacao, diretorio_saida, fonte, data_inicio, data_fim)
                    results.append({'file_name': os.path.basename(file_path), 'file_path': settings.MEDIA_URL + os.path.relpath(file_path, settings.MEDIA_ROOT)})
                except Exception as e:
                    results.append({'file_name': None, 'file_path': None, 'error': str(e)})
            
            return JsonResponse({'success': True, 'results': results})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})



def serve_csv(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, 'saida', filename)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
    else:
        return HttpResponse("Arquivo não encontrado.", status=404)




def csv_view(request, file_name, file_path):
    file_path = unquote(file_path.replace('-', '/'))
    
    # Lista todos os arquivos na pasta 'saida'
    output_dir = os.path.join(settings.MEDIA_ROOT, 'saida')
    csv_files = [f for f in os.listdir(output_dir) if f.endswith('.csv')]
    
    # Caminho completo do arquivo CSV selecionado
    full_file_path = os.path.join(output_dir, file_name)
    
    try:
        df = pd.read_csv(full_file_path, on_bad_lines='skip',  delimiter=';')
        table_html = df.to_html(classes='csv-table', index=False)
    except Exception as e:
        table_html = f"<p>Não foi encontrado dados dessa estação!</p>"
    
    return render(request, 'csv_page.html', {
        'file_name': file_name,
        'file_path': file_path,
        'csv_files': csv_files,
        'table_html': table_html
    })








