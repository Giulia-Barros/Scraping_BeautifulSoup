import requests
import pandas as pd
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO, filename="console.log", format="%(asctime)s - %(levelname)s = %(message)s")

 
DOMINIO = 'https://quotes.toscrape.com'
CABECALHO = {'User-Agent': 'Mozilla/5.0'}

pagina = 1
URL = f'{DOMINIO}/page/{pagina}/'


# TRAZ O CONTEÚDO DA PÁGINA
def conteudo_pagina(url, cabecalho):
    resposta = requests.get(url, headers=cabecalho).text
    dados_dominio = BeautifulSoup(resposta, 'html.parser')
    return dados_dominio


def analisa_citacoes():
    #FAZ A BUSCA POR LINHA
    logging.info(f'Iniciando Analise')
    citacoes = []
    pagina = 1

    #VALIDA SE TEM DADOS NA PAGINA
    while True:
        logging.info(f'Acessando a pagina {pagina}')
        url = f'{DOMINIO}/page/{pagina}/'
        dados_dominio = conteudo_pagina(url, CABECALHO) 

        linhas = dados_dominio.find_all('div', class_='quote')
        if not linhas:
            logging.info(f'Nenhuma citacao encontrada!')
            break

        logging.info(f'Foram encontradas {len(linhas)} citacoes na pagina {pagina}')    

        for linha in linhas:
            nome_autor = linha.find(class_='author').text
            frase = linha.find(class_='text').text

            about = linha.find('a') 
            link_autor = DOMINIO + about['href']

            tag_links = linha.find('div', class_='tags').find_all('a', class_='tag')
            link_tag = [DOMINIO + tag['href'] for tag in tag_links]
            nome_tag = [tag.get_text(strip=True) for tag in tag_links]

            citacao = {
                'Nome do autor': nome_autor,
                'Citação': frase,
                'Detalhes do autor': link_autor,
                'Tags': nome_tag,
                'Link tags': link_tag
            }

       
            citacoes.append(citacao)
        
        pagina += 1
        logging.info(f'Total de citacoes analisadas: {len(citacoes)}')

    return citacoes


df_citacoes = pd.json_normalize(analisa_citacoes())
print(df_citacoes)

