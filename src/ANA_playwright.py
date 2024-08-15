import os
import time
from playwright.sync_api import sync_playwright
import zipfile

diretorio_dados = "./data/"
diretorio_saida = "./data/saida/"
codigo_estacao = '1544050'

# Iniciar o Playwright
with sync_playwright() as p:
    # Abrir o navegador
    browser = p.chromium.launch(headless=False)
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
  
    
    # Interceptar o evento de download
    with page.expect_download() as download_info:
        # Clique no botão de download
        botao_download = page.locator('//*[@id="mat-tab-content-0-0"]/div/ana-card/mat-card/mat-card-content/ana-dados-convencionais-list/div/div[1]/table/tbody/tr/td[6]/button/span/mat-icon')
        botao_download.click()
        
    download = download_info.value
    
    # Definir o caminho onde o arquivo será salvo
    caminho_arquivo = os.path.join(diretorio_dados, codigo_estacao)
    download.save_as(caminho_arquivo)
    
    # Aguarde o download ser concluído
    while not any(fname.endswith('.zip') for fname in os.listdir(diretorio_dados)):
        time.sleep(1)
    
    # Localize o arquivo zip baixado
    arquivos_zip = [f for f in os.listdir(diretorio_dados) if f.endswith('.zip')]
    arquivo_zip = os.path.join(diretorio_dados, arquivos_zip[0])
    
    # Descompacte o arquivo ZIP
    with zipfile.ZipFile(arquivo_zip, 'r') as zip_ref:
        zip_ref.extractall(diretorio_saida)
    
    # Fechar o navegador
    browser.close()

# Localize o arquivo CSV descompactado
arquivos_csv = [f for f in os.listdir(diretorio_saida) if f.endswith('.csv')]
arquivo_csv = os.path.join(diretorio_saida, arquivos_csv[0])

print(f"Arquivo CSV descompactado: {arquivo_csv}")
