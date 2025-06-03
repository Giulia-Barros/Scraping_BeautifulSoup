# /***********************************************************************************
# |----------------------------------------------------------------------------------|
# |* Programa   | Quotes                                                            *|
# |----------------------------------------------------------------------------------|
# |* Autor      |  Giulia Barros                                                    *|
# |----------------------------------------------------------------------------------|
# |* Utilização | Raspagem de Dados                                                 *|
# |----------------------------------------------------------------------------------|
# |* Descricao  | Raspagem de dados do site Quotes to Scrape                        *|                                   
# |----------------------------------------------------------------------------------|
import requests
import pandas as pd
from bs4 import BeautifulSoup
import logging
import time

# Configuração do console.log
logging.basicConfig(level=logging.INFO, filename="console.log", format="%(asctime)s - %(levelname)s = %(message)s")

DOMINIO = 'https://quotes.toscrape.com'
CABECALHO = {'User-Agent': 'Mozilla/5.0'}

# Busca o conteúdo da página
def conteudo_pagina(url, cabecalho):
    resposta = requests.get(url, headers=cabecalho).text
    dados_dominio = BeautifulSoup(resposta, 'html.parser')
    return dados_dominio

# Busca os detalhes do autor, dentro do link encontrado na função analisa_citacoes()
def analisa_autor(url_autor):
    logging.info(f'Acessando detalhes do autor: {url_autor}')
    dados_autor = conteudo_pagina(url_autor, CABECALHO)

    nome = dados_autor.find('h3', class_='author-title').text.strip()
    nascimento = dados_autor.find('span', class_='author-born-date').text.strip()
    local_nascimento = dados_autor.find('span', class_='author-born-location').text.strip()
    descricao = dados_autor.find('div', class_='author-description').text.strip()

    return {
        'Nome completo': nome,
        'Data de nascimento': nascimento,
        'Local de nascimento': local_nascimento,
        'Descrição': descricao,
        'Link do autor': url_autor
    }

# Realiza a busca dos dados das citações
def analisa_citacoes():
    logging.info(f'Iniciando Analise')
    citacoes = []
    autores = {}  
    pagina = 1

    # Valida se há dados na página
    while True:
        logging.info(f'Acessando a pagina {pagina}')
        url = f'{DOMINIO}/page/{pagina}/'
        dados_citacoes = conteudo_pagina(url, CABECALHO) 

        linhas = dados_citacoes.find_all('div', class_='quote')
        if not linhas:
            logging.info(f'Nenhuma citacao encontrada!')
            break

        # Inicia a rapagem das citações
        for linha in linhas:
            nome_autor = linha.find(class_='author').text
            frase = linha.find(class_='text').text
            about = linha.find('a') 
            link_autor = DOMINIO + about['href']

            tag_links = linha.find('div', class_='tags').find_all('a', class_='tag')
            link_tag = [DOMINIO + tag['href'] for tag in tag_links]
            nome_tag = [tag.get_text(strip=True) for tag in tag_links]

            # Armazena citação
            citacoes.append({
                'Nome do autor': nome_autor,
                'Citação': frase,
                'Detalhes do autor': link_autor,
                'Tags': nome_tag,
                'Link tags': link_tag
            })

            # Se o autor ainda não foi processado, adiciona aos detalhes
            if nome_autor not in autores:
                detalhes = analisa_autor(link_autor)
                autores[nome_autor] = detalhes
                time.sleep(0.5) # Aguarda antes de continuar para evitar sobrecarga

        pagina += 1
        logging.info(f'Total de citacoes ate agora: {len(citacoes)}')

    return citacoes, list(autores.values())

# Execução
citacoes, autores = analisa_citacoes()

# Traz os resultados de forma alinhada, uma dataframe para cada função
df_citacoes = pd.DataFrame(citacoes)
df_autores = pd.DataFrame(autores)

# Faz a exportação para o CSV
df_citacoes.to_csv('citacoes.csv', index=False, encoding='utf-8-sig')
df_autores.to_csv('autores.csv', index=False, encoding='utf-8-sig')


# Exibe os resultados 5 primeiros resultados de cada função
print("Citações Detalhadas:")
print(df_citacoes.head())

print("\nAutores Detalhados:")
print(df_autores.head())

