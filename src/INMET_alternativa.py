import requests
from bs4 import BeautifulSoup

# URL para a qual vamos fazer a requisição
url = "https://apitempo.inmet.gov.br/estacao/front/"

# Dados do payload
payload = {
    'data_inicio': "2024-05-22",
    'data_fim': "2024-06-05",
    'estacao': "A526",
    'seed': "6OsXwKYF9YHarijHswS0ACY54NiK4babXLRgpx6rSP1Hj3ygcc&eUZUMGc1RlpRNUlhRm5VQTZ3UDNTSEVDbmRjV2U0Y3RZWkRhQ3k1bGsyUVpoVk1aNlgNk9zWHdLWUY5WUhhcmlqSHN3UzBBQ1k1NE5pSzRiYWJYTFJncHg2clNQMUhqM3lnY2M=",
    'gcap': "03AFcWeA72Yx2x7x4Rw-zNR9_yzQj0aHYDK4CNm9dJ5A_rXyMKv2cVpbgSJLwOU4JTMvezUMqlld1hrP7ehJ_xmER8arQ80fD5O43lXI0hILNuA8Dh4fV9REpkI3CEQT91qqvXqI-e57lWKjAmYSfb7hkCp1I7uOdL3CGTAQq8nzLa0tn2kw0xTD-Vov1cLbp9OWJ0w63tN59QJ67oYyqK_slyHs9B1vmJJpB_TCEJmCHdNVI_SREly_OlxpNOV00bUAaBEx9f5ftqThCsOBVRd1745tAfe2u3raS5pND7vqLysjDPNpCOqFbX-ey7OrFA6SZWAxnMeVw8m1vFe3UtroWjtvjDOn_VML6r2uXNRD_kwchZJSt8UQh2tNfizY3p3AY63T8wt7DrAlX6CO5VedAa5tIIGxQXFNoGQrhAztVJ4AyBKz6f2vKzcQQIfyioliNhVHSwEuyssQlrHSH4FMsaqPgDt-wjdLvh-L0JQ5fQ-34AFZ-1CF0wmfmk1yi1c6cxU81ONnKrw9uyB-v7uBIjY6CIbf8U6cQYIW8S05SOpOTPCDpkxgGe1DUBseu7RemLTT6Ci967VHdf_assxJkcPF07H5uxG38bHmV8eC9tTjRxTHadOSiGhcsCBzBW2b4pKNmVpa35IQIK95j3xYoGJxPGpjHy84bztKbQwm84tRWOO1VIwbr50OOwHyPvhIHEUuyhWihL"
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Referer': 'https://tempo.inmet.gov.br/',
    'Content-Type': 'application/json',
    'Origin': 'https://tempo.inmet.gov.br',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'pt-PT,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Sec-Ch-Ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site'
}

# Fazendo a requisição POST
response = requests.post(url, data=payload,  headers=headers)

# Verificando se a requisição foi bem sucedida
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    print(soup)

    # tabelas = soup.find_all('table')
    # for tabela in tabelas:
    #     print(tabela.prettify())

else:
    print(f"Falha na requisição: {response.status_code}")
    print(response.text) 
 