import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import zipfile

diretorio_dados = "./data/"
diretorio_saida = "./data/saida/"

# Endereco do driver do browser
folder_chrome_driver = './drive selenium/chromedriver.exe'

# Para desabilitar a abertura de uma nova janela do browser pelo Selenium
chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": os.path.abspath(diretorio_dados)
})

driver = webdriver.Chrome(options=chrome_options)
driver.get('https://www.snirh.gov.br/hidroweb/serieshistoricas')

time.sleep(3)

# Encontre o campo de código de estação e preencha com o código desejado
codigo_estacao = "1544011"  # Substitua pelo código da estação desejada
campo_codigo_estacao = driver.find_element(By.XPATH, '//*[@id="mat-input-0"]')
campo_codigo_estacao.send_keys(codigo_estacao)

time.sleep(3)

# Clique no botão de busca
botao_busca = driver.find_element(By.XPATH, '/html/body/app-root/mat-sidenav-container/mat-sidenav-content/ng-component/form/ana-card/mat-card/mat-card-content/mat-card-actions/div/div/button[1]/span')
botao_busca.click()

# Aguarde um momento para a página carregar
time.sleep(5)  # Você pode ajustar esse valor conforme necessário

# Clique no botão de download
botao_download = driver.find_element(By.XPATH, '//*[@id="mat-tab-content-0-0"]/div/ana-card/mat-card/mat-card-content/ana-dados-convencionais-list/div/div/table/tbody/tr/td[5]/button/span/mat-icon')
botao_download.click()
time.sleep(10)

# Aguarde o download ser concluído
while not any(fname.endswith('.zip') for fname in os.listdir(diretorio_dados)):
    time.sleep(1)

# Localize o arquivo zip baixado
arquivos_zip = [f for f in os.listdir(diretorio_dados) if f.endswith('.zip')]
arquivo_zip = os.path.join(diretorio_dados, arquivos_zip[0])

# Descompacte o arquivo ZIP
with zipfile.ZipFile(arquivo_zip, 'r') as zip_ref:
    zip_ref.extractall(diretorio_saida)

# Feche o navegador
driver.quit()

# Localize o arquivo CSV descompactado
arquivos_csv = [f for f in os.listdir(diretorio_saida) if f.endswith('.csv')]
arquivo_csv = os.path.join(diretorio_saida, arquivos_csv[0])

print(f"Arquivo CSV descompactado: {arquivo_csv}")
