
import os
import time
import requests


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains



from bs4 import BeautifulSoup


#Endereco do driver do browser 
folder_chrome_driver='./drive selenium/chromedriver.exe'

#Para desabilitar a abertura de uma nova janela do browser pelo Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")


VALOR_ESTACAO='A559' #Januária - MG

DATA_INIT='22/11/2023'
DATA_END='22/01/2024'


browser = webdriver.Chrome()
browser.get(f'https://tempo.inmet.gov.br/TabelaEstacoes/{VALOR_ESTACAO}')

time.sleep(3)


# abre menu lateral
browser.find_element(By.XPATH, '//*[@id="root"]/div[1]/div[1]/i').click()

time.sleep(3)
#Selecionamos a opção de estação automática
browser.find_element(By.XPATH, '//button[text()="Automáticas"]').click()


#Primeiro limpados o formulário e então preenchemos com a data inicial que desejamos.
browser.find_element(By.XPATH, '//*[@id="root"]/div[2]/div[1]/div[2]/div[4]/input').clear()
browser.find_element(By.XPATH, '//*[@id="root"]/div[2]/div[1]/div[2]/div[4]/input').send_keys(DATA_INIT)
 


# #O mesmo para a data final
browser.find_element(By.XPATH, '//*[@id="root"]/div[2]/div[1]/div[2]/div[5]/input').clear()
browser.find_element(By.XPATH, '//*[@id="root"]/div[2]/div[1]/div[2]/div[5]/input').send_keys(DATA_END)
 
# #Por fim, clicamos em "gerar tabela"
browser.find_element(By.XPATH,'//*[@id="root"]/div[2]/div[1]/div[2]/button').click()

time.sleep(3)

# baixando o csv com os dados
botao_download   = browser.find_element(By.XPATH,'//*[@id="root"]/div[2]/div[2]/div/div/div/span/a')

path_file = f'./data/base_{VALOR_ESTACAO}_{DATA_INIT}_{DATA_END}'

browser.execute_script("arguments[0].setAttribute('download', '{}')".format(f'base_{VALOR_ESTACAO}_{DATA_INIT}_{DATA_END}'), botao_download)
botao_download.click()

time.sleep(3)

# Espere até que o arquivo seja baixado
while not os.path.exists(path_file):
    pass

# Feche o navegador
browser.quit()






