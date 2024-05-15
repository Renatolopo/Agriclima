import sys
import csv
import os

# Adicione o caminho do seu projeto ao sys.path
caminho_projeto = './AgriClima'
sys.path.append(caminho_projeto)

# Importe o shell do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AgriClima.settings')
import django
django.setup()

from AppAgriClima.models import Estacao

def popular_tabela_com_csv(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo_csv:
        leitor_csv = csv.reader(arquivo_csv)
        # Ignorar o cabeçalho se houver
        next(leitor_csv)
        for linha in leitor_csv:
            # Supondo que a ordem das colunas no CSV seja a mesma que a ordem dos campos no modelo
            id, nome, codigo, tipo_estacao, latitude,longitude, fonte = linha
            
            # Criar uma nova instância do modelo Estacao
            nova_estacao = Estacao(
                codigo=codigo,
                nome=nome,
                latitude=latitude,
                longitude=longitude,
                tipoEstacao=tipo_estacao,
                fonte=fonte
            )
            # Salvar a instância no banco de dados
            nova_estacao.save()

# Chamada da função para popular a tabela com o arquivo CSV
popular_tabela_com_csv('../../data/Estacao_tratada.csv', )