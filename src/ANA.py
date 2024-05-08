import requests
import pandas as pd

data_inicio = "01/01/2010"
data_fim = "31/12/2023"

tipo_dado = "2"  # 1-Cota, 2-Chuva ou 3-Vazão
nivel_consistencia = "1"  # 1-Bruto ou 2-Consistido (é feito o download independente do nível de consistência)

lista = ["01443001", "01641010", "01646000"]


for codigo in lista:
    link = f"http://telemetriaws1.ana.gov.br/ServiceANA.asmx/HidroSerieHistorica?codEstacao={codigo}&dataInicio={data_inicio}&dataFim={data_fim}&tipoDados={tipo_dado}&nivelConsistencia={nivel_consistencia}"
    response = requests.get(link)

    print(link)

    # if response.status_code == 200:
    #     dados_xml = response.text
    #     df_con = pd.read_xml(dados_xml, xpath=".//SerieHistorica")
    #     if not df_con.empty:
    #         df_con = df_con.iloc[:, :46]

    #         df_con.to_excel(f"data/base_chuva_{codigo}.xlsx", index=False)
    #     else:
    #         print(f"Estação sem dados: {codigo}")
