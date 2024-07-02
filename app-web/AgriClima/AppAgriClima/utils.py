# utils.py
import requests
import zipfile
import io
import os
import time
from django.conf import settings

import shutil

def download_station_data(codigo_estacao, nome_estacao, diretorio_saida, max_retries=5, backoff_factor=1):
    url = 'https://www.snirh.gov.br/hidroweb/rest/api/documento/download/files'

    cookies = {
        'ASP.NET_SessionId': 'ikp1p3njs324yel24t1hukyc',
        '27628ed70890f724c98c0800461fb776': 'bc84d6fd8f8fe62e432a5ea4812337b9',
        'c82026e9a6b8da54e034dc38d01ba2a4': 'c792c4a30833ad8853eda3b70e64e606',
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'pt-PT,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'priority': 'u=0, i',
        'referer': 'https://www.snirh.gov.br/hidroweb/serieshistoricas',
        'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    }

    params = {
        'tipodocumento': 'csv',
        'codigoestacao': codigo_estacao,
        'forcenewfiles': 'N',
    }

    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, cookies=cookies, headers=headers, timeout=10)

            if response.status_code == 200:
                content_type = response.headers.get('Content-Type')
                print(f"Content-Type: {content_type}")

                if len(response.content) == 0:
                    print("O arquivo baixado está vazio.")
                    return

                try:
                    zip_file = zipfile.ZipFile(io.BytesIO(response.content))
                    file_list = zip_file.namelist()
                    print(f"Arquivos no ZIP: {file_list}")

                    for file_name in file_list:
                        if file_name.endswith('.csv'):
                            if not os.path.exists(diretorio_saida):
                                os.makedirs(diretorio_saida)

                            output_file_path = os.path.join(diretorio_saida, f"{nome_estacao}_{codigo_estacao}.csv")

                            with zip_file.open(file_name) as csv_file:
                                raw_data = csv_file.read()
                                decoded_data = raw_data.decode('latin-1')
                                lines = decoded_data.split('\n')

                                header_index = next((i for i, line in enumerate(lines) if line.startswith("EstacaoCodigo")), None)

                                if header_index is not None:
                                    clean_data = "\n".join(lines[header_index:])

                                    with open(output_file_path, 'w', encoding='latin-1') as f_out:
                                        f_out.write(clean_data)

                                    print(f"Arquivo CSV salvo em: {output_file_path}")
                                    return output_file_path
                                else:
                                    print("Cabeçalho 'EstacaoCodigo' não encontrado.")
                                    return "Cabeçalho 'EstacaoCodigo' não encontrado."

                    return "Nenhum arquivo CSV encontrado no ZIP."
                except zipfile.BadZipFile:
                    print("O arquivo baixado não é um arquivo ZIP válido.")
                    return "O arquivo baixado não é um arquivo ZIP válido."
            else:
                print(f"Falha ao baixar arquivo. Status code: {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"Erro na tentativa {attempt + 1}: {e}")

        # Calcular o tempo de espera exponencial
        sleep_time = backoff_factor * (2 ** attempt)
        print(f"Aguardando {sleep_time} segundos antes da próxima tentativa...")
        time.sleep(sleep_time)

    raise Exception(f"Falha ao baixar arquivo após {max_retries} tentativas.")




def clear_output_directory(directory_path):
    if os.path.exists(directory_path):
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')




