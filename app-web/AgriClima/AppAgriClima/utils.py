# utils.py
import requests
import zipfile
import io
import os
import time
from django.conf import settings

import shutil

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException, TimeoutException, NoSuchElementException



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



def download_multiple_stations(stations, output_dir):
    results = []
    for station in stations:
        file_path = download_station_data(station['codigo'], station['nome'].replace(" ", "_"), output_dir)
        results.append(file_path)
    return results



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



def download_station_data_inmet(codigo_estacao, nome_estacao, diretorio_saida, data_inicio, data_fim):
    diretorio_dados = os.path.abspath(diretorio_saida)
    folder_chrome_driver = '../../drive selenium/chromedriver.exe'

    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Modo headless
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": diretorio_dados,
        "profile.default_content_settings.popups": 0,
        "download.prompt_for_download": False,
        "directory_upgrade": True,
    })

    service = Service(folder_chrome_driver)
    browser = webdriver.Chrome(service=service, options=chrome_options)
    browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': '''
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        '''
    })

    try:
        browser.get(f'https://tempo.inmet.gov.br/TabelaEstacoes/{codigo_estacao}')
        time.sleep(3)

        browser.find_element(By.XPATH, '//*[@id="root"]/div[1]/div[1]/i').click()
        time.sleep(3)

        browser.find_element(By.XPATH, '//button[text()="Automáticas"]').click()

        browser.find_element(By.XPATH, '//*[@id="root"]/div[2]/div[1]/div[2]/div[4]/input').clear()
        browser.find_element(By.XPATH, '//*[@id="root"]/div[2]/div[1]/div[2]/div[4]/input').send_keys(data_inicio)

        browser.find_element(By.XPATH, '//*[@id="root"]/div[2]/div[1]/div[2]/div[5]/input').clear()
        browser.find_element(By.XPATH, '//*[@id="root"]/div[2]/div[1]/div[2]/div[5]/input').send_keys(data_fim)

        browser.find_element(By.XPATH, '//*[@id="root"]/div[2]/div[1]/div[2]/button').click()

        try:
            botao_download = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div[2]/div[2]/div/div/div/span/a'))
            )
            file_name = f'{nome_estacao}_{codigo_estacao}.csv'
            browser.execute_script("arguments[0].setAttribute('download', '{}')".format(file_name), botao_download)
            botao_download.click()
            time.sleep(3)  # Tempo para garantir que o download seja concluído

            downloaded_file = os.path.join(diretorio_dados, file_name)
            if os.path.exists(downloaded_file):
                print(f"Arquivo CSV salvo em: {downloaded_file}")
                return downloaded_file
            else:
                print("O arquivo CSV não foi encontrado após o download.")
                return "O arquivo CSV não foi encontrado após o download."
        except TimeoutException:
            print("O botão de download não foi encontrado no tempo esperado.")
            return "O botão de download não foi encontrado no tempo esperado."
        except UnexpectedAlertPresentException as e:
            print("Alerta inesperado presente: ", e.alert_text)
            alert = Alert(browser)
            alert.accept()
            time.sleep(3)
            try:
                botao_download = WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div[2]/div[2]/div/div/div/span/a'))
                )
                browser.execute_script("arguments[0].setAttribute('download', '{}')".format(file_name), botao_download)
                botao_download.click()
                time.sleep(3)  # Tempo para garantir que o download seja concluído

                downloaded_file = os.path.join(diretorio_dados, file_name)
                if os.path.exists(downloaded_file):
                    print(f"Arquivo CSV salvo em: {downloaded_file}")
                    return downloaded_file
                else:
                    print("O arquivo CSV não foi encontrado após o download.")
                    return "O arquivo CSV não foi encontrado após o download."
            except (TimeoutException, NoSuchElementException) as e:
                print("Erro ao tentar clicar no botão de download novamente: ", e)
                return "Erro ao tentar clicar no botão de download novamente: " + str(e)
    finally:
        time.sleep(3)
        browser.quit()



def download_station_data_general(codigo_estacao, nome_estacao, diretorio_saida, fonte, data_inicio=None, data_fim=None):
    if fonte == 'ANA':
        return download_station_data(codigo_estacao, nome_estacao, diretorio_saida)
    elif fonte == 'INMET':
        return download_station_data_inmet(codigo_estacao, nome_estacao, diretorio_saida, data_inicio, data_fim)
    else:
        raise ValueError("Fonte desconhecida")

