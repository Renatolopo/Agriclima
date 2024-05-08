
import os
import sys
from django.conf import settings

# Adicione o diretório do projeto ao sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurar as configurações do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AgriClima.settings')
settings.configure()

# Importar e configurar o Django após a configuração
import django
django.setup()

import pandas as pd
import csv
from AppAgriClima.models import Estacao


def carregar_dados_csv():
    with open('../../data/Estacao_tratada.csv', 'r', encoding='latin-1') as f:
        reader = csv.reader(f)
        next(reader)  # Ignorar cabeçalho
        for row in reader:
            x , codigo, nome, latitude, longitude, tipoEstacao = row
            Estacao.objects.create(codigo=codigo, nome=nome, latitude=latitude, longitude=longitude, tipoEstacao=tipoEstacao)
            Estacao.save()
carregar_dados_csv()