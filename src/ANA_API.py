import requests
import zipfile
import io
import os
import time

def download_station_data(codigo_estacao, diretorio_saida, max_retries=5, backoff_factor=1):
    url = 'https://www.snirh.gov.br/hidroweb/rest/api/documento/download/files'
    
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJleHAiOjE3MjM1OTQ1NTYsImlhdCI6MTcyMzU5Mzk1Nn0.VJOXh_wMntF-6ginOXG7XZni53PcD9if_VJHW06n3Lbd1-iaCtwt2X4zAw6TCJvSJXDqfro_eyOtVv51DIelKQ',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    }

    params = {
        'tipodocumento': 'csv',
        'codigoestacao': codigo_estacao,
        'forcenewfiles': 'N',
    }

    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)
            print(f"Request URL: {response.url}")
            print(f"Request Headers: {response.request.headers}")
            print(f"Response Status Code: {response.status_code}")
            print(f"Response Text: {response.text}")
            
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
                            
                            output_file_path = os.path.join(diretorio_saida, f"{codigo_estacao}_data.csv")
                            
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
        
        sleep_time = backoff_factor * (2 ** attempt)
        print(f"Aguardando {sleep_time} segundos antes da próxima tentativa...")
        time.sleep(sleep_time)

    raise Exception(f"Falha ao baixar arquivo após {max_retries} tentativas.")

# Exemplo de uso
codigo_estacao = '1444011'
diretorio_saida = "./data/saida/"
output_file_path = download_station_data(codigo_estacao, diretorio_saida)
print(output_file_path)
