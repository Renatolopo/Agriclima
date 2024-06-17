import os
import time
import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import UnexpectedAlertPresentException, NoAlertPresentException, TimeoutException, NoSuchElementException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

diretorio_dados = "./data/"

# Endereco do driver do browser 
folder_chrome_driver='./drive selenium/chromedriver.exe'

# Para desabilitar a abertura de uma nova janela do browser pelo Selenium
chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": os.path.abspath(diretorio_dados)
})

VALOR_ESTACAO = 'A526'  # Januária - MG
DATA_INIT = '22/11/2023'
DATA_END = '22/01/2024'

# browser = webdriver.Chrome(executable_path='./drive selenium/chromedriver.exe')
browser = webdriver.Chrome(options=chrome_options)
browser.get(f'https://tempo.inmet.gov.br/TabelaEstacoes/{VALOR_ESTACAO}')

time.sleep(3)

# Abre menu lateral
browser.find_element(By.XPATH, '//*[@id="root"]/div[1]/div[1]/i').click()

time.sleep(3)

# Selecionamos a opção de estação automática
browser.find_element(By.XPATH, '//button[text()="Automáticas"]').click()

# Primeiro limpamos o formulário e então preenchemos com a data inicial que desejamos.
browser.find_element(By.XPATH, '//*[@id="root"]/div[2]/div[1]/div[2]/div[4]/input').clear()
browser.find_element(By.XPATH, '//*[@id="root"]/div[2]/div[1]/div[2]/div[4]/input').send_keys(DATA_INIT)

# O mesmo para a data final
browser.find_element(By.XPATH, '//*[@id="root"]/div[2]/div[1]/div[2]/div[5]/input').clear()
browser.find_element(By.XPATH, '//*[@id="root"]/div[2]/div[1]/div[2]/div[5]/input').send_keys(DATA_END)

# Por fim, clicamos em "gerar tabela"
browser.find_element(By.XPATH, '//*[@id="root"]/div[2]/div[1]/div[2]/button').click()

try:
    # Espera até que o botão de download esteja presente
    botao_download = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div[2]/div[2]/div/div/div/span/a'))
    )
    browser.execute_script("arguments[0].setAttribute('download', '{}')".format(f'base_{VALOR_ESTACAO}_{DATA_INIT}_{DATA_END}'), botao_download)
    botao_download.click()
except TimeoutException:
    print("O botão de download não foi encontrado no tempo esperado.")
except UnexpectedAlertPresentException as e:
    # Captura e aceita o alerta
    print("Alerta inesperado presente: ", e.alert_text)
    alert = Alert(browser)
    alert.accept()
    # Adiciona um tempo de espera e tenta encontrar o botão novamente
    time.sleep(3)
    try:
        botao_download = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div[2]/div[2]/div/div/div/span/a'))
        )
        browser.execute_script("arguments[0].setAttribute('download', '{}')".format(f'base_{VALOR_ESTACAO}_{DATA_INIT}_{DATA_END}'), botao_download)
        botao_download.click()
    except (TimeoutException, NoSuchElementException) as e:
        print("Erro ao tentar clicar no botão de download novamente: ", e)
finally:
    time.sleep(3)
    # Feche o navegador
    browser.quit()
