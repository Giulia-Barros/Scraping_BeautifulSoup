import requests
import pandas as pd
from bs4 import BeautifulSoup
from itertools import product
 
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
    citacoes = []
    pagina = 1

    #VALIDA SE TEM DADOS NA PAGINA
    while True:
        url = f'{DOMINIO}/page/{pagina}/'
        dados_dominio = conteudo_pagina(url, CABECALHO) 
        linhas = dados_dominio.find_all('div', class_='quote')

        if not linhas:
            break

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

    return citacoes


df_citacoes = pd.json_normalize(analisa_citacoes())
print(df_citacoes)

