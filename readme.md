# Agriclima

Agriclima é um projeto acadêmico que está sendo desenvolvido, com o objetivo de coletar dados climáticos de diversas estações e realizar previsões de dados faltantes para auxiliar engenheiros agrícolas em suas análises e tomadas de decisão.

## Descrição

O Agriclima consiste em um conjunto de scripts Python que fazem a coleta de dados climáticos de estações específicas, utilizando a API disponibilizada pela Agência Nacional de Águas (ANA) e Instituto Nacional de Meteorologia (INMET). Os dados coletados incluem informações sobre chuva, cota e vazão, permitindo uma análise abrangente das condições climáticas em diferentes regiões.

## Como Funciona

O projeto conta com um script principal, `ANA.py`, que realiza a coleta de dados climáticos de acordo com os parâmetros especificados, como intervalo de datas, tipo de dado e nível de consistência. Atualmente, o foco está na coleta de dados de chuva, mas o projeto ainda está em desenvolvimento

## Requisitos

- Python 3.x
- Bibliotecas Python: requests, pandas

## Uso

1. Clone este repositório:

`git clone https://github.com/Renatolopo/agriclima.git`

2. Instale as dependências:

`pip install -r requirements.txt`

3. Execute o script principal para coletar os dados climáticos:

