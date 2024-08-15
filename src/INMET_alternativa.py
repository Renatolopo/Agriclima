import os
import time
from playwright.sync_api import sync_playwright

diretorio_dados = "./data/"

VALOR_ESTACAO = 'A539'
DATA_INIT = '2023-11-21'
DATA_END = '2024-01-21'

def handle_alert(page):
    try:
        page.on("dialog", lambda dialog: dialog.accept())
        return True
    except:
        return False

def carregar_tabela():
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

        page.goto(f'https://tempo.inmet.gov.br/TabelaEstacoes/{VALOR_ESTACAO}')
        time.sleep(3)  # Aumentando o tempo de espera para garantir que a página carregue completamente

        

        page.locator('//*[@id="root"]/div[1]/div[1]/i').click()
        time.sleep(3)

        # Adicionando verificação de visibilidade
        automatics_button = page.locator('//button[text()="Automáticas"]')
        automatics_button.wait_for(state="visible", timeout=60000)
        automatics_button.click()

       

        page.locator('//*[@id="root"]/div[2]/div[1]/div[2]/div[4]/input').fill(DATA_INIT)
        page.locator('//*[@id="root"]/div[2]/div[1]/div[2]/div[5]/input').fill(DATA_END)
        page.locator('//*[@id="root"]/div[2]/div[1]/div[2]/button').click()

        

        try:
            botao_download = page.wait_for_selector('//*[@id="root"]/div[2]/div[2]/div/div/div/span/a', timeout=30000)

            # Listener para o evento de download
            with page.expect_download() as download_info:
                page.evaluate('button => button.setAttribute("download", "base_' + VALOR_ESTACAO + '_' + DATA_INIT + '_' + DATA_END + '")', botao_download)
                botao_download.click()
            
            download = download_info.value
            download_path = os.path.join(diretorio_dados, download.suggested_filename)
            download.save_as(download_path)
            print(f"Arquivo baixado em: {download_path}")
        except Exception as e:
            
            print("O botão de download não foi encontrado no tempo esperado ou houve um erro: ", e)

        time.sleep(3)
        browser.close()

if __name__ == "__main__":
    carregar_tabela()
