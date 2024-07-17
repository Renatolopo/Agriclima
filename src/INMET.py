import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException, TimeoutException, NoSuchElementException

diretorio_dados = "./data/"
folder_chrome_driver = './drive selenium/chromedriver.exe'

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
    "download.default_directory": os.path.abspath(diretorio_dados),
    "profile.default_content_settings.popups": 0,
    "download.prompt_for_download": False,
    "directory_upgrade": True,
})

VALOR_ESTACAO = 'A539'  
DATA_INIT = '22/11/2023'
DATA_END = '22/01/2024'

service = Service(folder_chrome_driver)
browser = webdriver.Chrome(service=service, options=chrome_options)
browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
    'source': '''
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
    '''
})

def carregar_tabela():
    try:
        browser.get(f'https://tempo.inmet.gov.br/TabelaEstacoes/{VALOR_ESTACAO}')
        time.sleep(3)

        browser.find_element(By.XPATH, '//*[@id="root"]/div[1]/div[1]/i').click()
        time.sleep(3)

        browser.find_element(By.XPATH, '//button[text()="Automáticas"]').click()

        browser.find_element(By.XPATH, '//*[@id="root"]/div[2]/div[1]/div[2]/div[4]/input').clear()
        browser.find_element(By.XPATH, '//*[@id="root"]/div[2]/div[1]/div[2]/div[4]/input').send_keys(DATA_INIT)

        browser.find_element(By.XPATH, '//*[@id="root"]/div[2]/div[1]/div[2]/div[5]/input').clear()
        browser.find_element(By.XPATH, '//*[@id="root"]/div[2]/div[1]/div[2]/div[5]/input').send_keys(DATA_END)

        browser.find_element(By.XPATH, '//*[@id="root"]/div[2]/div[1]/div[2]/button').click()

        try:
            botao_download = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div[2]/div[2]/div/div/div/span/a'))
            )
            browser.execute_script("arguments[0].setAttribute('download', '{}')".format(f'base_{VALOR_ESTACAO}_{DATA_INIT}_{DATA_END}'), botao_download)
            botao_download.click()
        except TimeoutException:
            print("O botão de download não foi encontrado no tempo esperado.")
        except UnexpectedAlertPresentException as e:
            print("Alerta inesperado presente: ", e.alert_text)
            alert = Alert(browser)
            alert.accept()
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
        browser.quit()

if __name__ == "__main__":
    carregar_tabela()
