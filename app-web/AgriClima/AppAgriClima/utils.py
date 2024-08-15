# utils.py
import requests
import zipfile
import io
import os
import time
from django.conf import settings

import shutil

from playwright.sync_api import sync_playwright
from datetime import datetime



def download_station_data(codigo_estacao, nome_estacao, diretorio_saida, max_retries=5, backoff_factor=1):
    # Iniciar o Playwright
    with sync_playwright() as p:
        # Abrir o navegador
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        
        # Abrir uma nova página
        page = context.new_page()
        
        # Navegar até a página desejada
        page.goto('https://www.snirh.gov.br/hidroweb/serieshistoricas')
        
        # Encontre o campo de código de estação e preencha com o código desejado
        campo_codigo_estacao = page.locator('xpath=//*[@id="mat-input-0"]')
        campo_codigo_estacao.fill(codigo_estacao)
        
        # Clique no botão de busca
        botao_busca = page.locator('xpath=/html/body/app-root/mat-sidenav-container/mat-sidenav-content/ng-component/form/ana-card/mat-card/mat-card-content/mat-card-actions/div/div/button[1]/span')
        botao_busca.click()
        
        # Tentar realizar o download com número máximo de tentativas
        for attempt in range(max_retries):
            try:
                # Interceptar o evento de download
                with page.expect_download() as download_info:
                    # Clique no botão de download
                    botao_download = page.locator('//*[@id="mat-tab-content-0-0"]/div/ana-card/mat-card/mat-card-content/ana-dados-convencionais-list/div/div[1]/table/tbody/tr/td[6]/button/span/mat-icon')
                    botao_download.click()
                
                download = download_info.value
                
                # Definir o caminho onde o arquivo será salvo
                caminho_arquivo = os.path.join(diretorio_saida, f"{nome_estacao}_{codigo_estacao}.zip")
                download.save_as(caminho_arquivo)
                
                # Aguarde o download ser concluído
                while not any(fname.endswith('.zip') for fname in os.listdir(diretorio_saida)):
                    time.sleep(1)
                
                # Localize o arquivo zip baixado
                if not os.path.exists(caminho_arquivo):
                    print("Erro ao localizar o arquivo baixado.")
                    return "Erro ao localizar o arquivo baixado."
                
                # Descompacte o arquivo ZIP
                with zipfile.ZipFile(caminho_arquivo, 'r') as zip_ref:
                    file_list = zip_ref.namelist()
                    print(f"Arquivos no ZIP: {file_list}")
                    
                    for file_name in file_list:
                        if file_name.endswith('.csv'):
                            if not os.path.exists(diretorio_saida):
                                os.makedirs(diretorio_saida)
                                
                            output_file_path = os.path.join(diretorio_saida, f"{nome_estacao}_{codigo_estacao}.csv")
                            
                            with zip_ref.open(file_name) as csv_file:
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
            except Exception as e:
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


def handle_alert(page):
    try:
        page.on("dialog", lambda dialog: dialog.accept())
        return True
    except:
        return False
    
def converter_data(data):
    # Converte a string para um objeto datetime
    data_obj = datetime.strptime(data, "%d/%m/%Y")
    # Converte o objeto datetime para uma string no formato desejado
    data_formatada = data_obj.strftime("%Y-%m-%d")
    return data_formatada

        
def download_station_data_inmet(codigo_estacao, nome_estacao, diretorio_saida, data_inicio, data_fim):
    diretorio_dados = os.path.abspath(diretorio_saida)
    data_inicio = converter_data(data_inicio)
    data_fim = converter_data(data_fim)

    print(f'diretorio: {diretorio_dados} Estacao: {codigo_estacao} Inicio: {data_inicio} Fim: {data_fim}')

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=[
            '--start-maximized',
            '--disable-blink-features=AutomationControlled',
            '--disable-web-security',
            '--disable-features=IsolateOrigins,site-per-process'
        ])  # Modo headless ativado com tela maximizada

        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
        )  # Definindo a resolução da tela e User-Agent

        page = context.new_page()

        # Modificações do navegador para esconder que está em modo headless
        page.add_init_script('''() => {
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
            Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
        }''')


        page.goto(f'https://tempo.inmet.gov.br/TabelaEstacoes/{codigo_estacao}')
        time.sleep(3)  # Aumentando o tempo de espera para garantir que a página carregue completamente

        page.locator('//*[@id="root"]/div[1]/div[1]/i').click()
        time.sleep(3)

        # Adicionando verificação de visibilidade
        automatics_button = page.locator('//button[text()="Automáticas"]')
        automatics_button.wait_for(state="visible", timeout=60000)
        automatics_button.click()

        time.sleep(2)
        print(page.locator('//*[@id="root"]/div[2]/div[1]/div[2]/div[4]/input'))

        page.locator('//*[@id="root"]/div[2]/div[1]/div[2]/div[4]/input').fill(data_inicio)
        page.locator('//*[@id="root"]/div[2]/div[1]/div[2]/div[5]/input').fill(data_fim)
        page.locator('//*[@id="root"]/div[2]/div[1]/div[2]/button').click()

        try:
            botao_download = page.wait_for_selector('//*[@id="root"]/div[2]/div[2]/div/div/div/span/a', timeout=30000)

            # Listener para o evento de download
            with page.expect_download() as download_info:
                page.evaluate('button => button.setAttribute("download", "' + f'{nome_estacao}_{codigo_estacao}.csv' + '")', botao_download)
                botao_download.click()

            download = download_info.value
            download_path = os.path.join(diretorio_dados, download.suggested_filename)
            download.save_as(download_path)
            print(f"Arquivo baixado em: {download_path}")
            return download_path
        except Exception as e:
            print("O botão de download não foi encontrado no tempo esperado ou houve um erro: ", e)
            return "O botão de download não foi encontrado no tempo esperado ou houve um erro: " + str(e)
        finally:
            time.sleep(3)
            browser.close()



def download_station_data_general(codigo_estacao, nome_estacao, diretorio_saida, fonte, data_inicio=None, data_fim=None):
    if fonte == 'ANA':
        return download_station_data(codigo_estacao, nome_estacao, diretorio_saida)
    elif fonte == 'INMET':
        return download_station_data_inmet(codigo_estacao, nome_estacao, diretorio_saida, data_inicio, data_fim)
    else:
        raise ValueError("Fonte desconhecida")

