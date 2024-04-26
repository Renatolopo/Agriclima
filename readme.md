# Agriclima

Agriclima é um projeto acadêmico que está sendo desenvolvido, com o objetivo de coletar dados climáticos de diversas estações e realizar previsões de dados faltantes para auxiliar engenheiros agrícolas em suas análises e tomadas de decisão.

## Descrição

O Agriclima consiste em um conjunto de scripts Python que fazem a coleta de dados climáticos de estações específicas, utilizando a API disponibilizada pela Agência Nacional de Águas (ANA) e Instituto Nacional de Meteorologia (INMET). Os dados coletados incluem informações sobre chuva, cota e vazão, permitindo uma análise abrangente das condições climáticas em diferentes regiões.

## Como Funciona

O projeto conta com 2 script principal, `ANA.py` e `INMET.py`, que realiza a coleta de dados climáticos de acordo com os parâmetros especificados, como intervalo de datas, tipo de dado e nível de consistência. Atualmente, o foco está na coleta de dados de chuva, mas o projeto ainda está em desenvolvimento

### Sobre os script: 
#### INMET.py
No script tem o codigo da estação, que está com o valor de Januária, mas pode ser alterado. Além disso também pode ser definido o intervalo de data dos dados, porém os intervalos podem ter no maximo 6 meses.  Quando esse projeto virar uma aplicação esses valores serão passados como parametros.

```python
VALOR_ESTACAO='A559' #Januária - MG

DATA_INIT='22/11/2023'
DATA_END='22/01/2024'

```

Após configurado esses campos basta executar o script que o arquivo de exportação estara no diretorio ‘./data’ como .csv com o nome seguindo essa estrutura `base_{VALOR_ESTACAO}_{DATA_INIT}_{DATA_END}` baseado nos valores das variáveis que foram ajustadas no inicio.

## Requisitos

- Python 3.x
- Bibliotecas Python: requests, pandas

## Uso

1. Clone este repositório:

`git clone https://github.com/Renatolopo/agriclima.git`

2. Instale as dependências:

`pip install -r requirements.txt`

3. Execute o script principal para coletar os dados climáticos:

