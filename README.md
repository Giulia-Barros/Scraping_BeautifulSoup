# Scraping BeautifulSoup

Projeto Python com interface gráfica que realiza a raspagem de dados do site [Quotes to Scrape](https://quotes.toscrape.com) utilizando a biblioteca **BeautifulSoup**. Traz as informações detalhadas das citações disponíveis e os dados relacionados a cada autor citado.

## Desenvolvedora

**Giulia Barros**

## Estrutura do Projeto
Scraping_BeautifulSoup/
├── quotes.py # Módulo de raspagem com BeautifulSoup
├── interface.py # Interface gráfica com CustomTkinter
├── console.log # Log das execuções
├── citacoes.csv # (Gerado após exportação)
├── autores.csv # (Gerado após exportação)
├── print.png # (Pode ser gerado após exportação)
└── README.md # Documentação do projeto

## 🔧 Tecnologias Utilizadas

- Python 3.x
- `requests`
- `BeautifulSoup (bs4)`
- `pandas`
- `CustomTkinter`
- `threading`
- `logging`
- `pyautogui`

## Funcionalidades

### `quotes.py` - Raspagem do Dados
- Extrai todas as citações disponíveis no site.
- Acessa perfis de autores e coleta nome completo, data/local de nascimento e descrição.
- Retorna dados estruturados em listas de dicionários.
- Exporta para CSV
- Registra atividades no `console.log`.

### `interface.py` – Interface Gráfica
- Botão para executar raspagem.
- Exibe os resultados em áreas de texto separadas para citações e autores.
- Botão para exportar os dados para arquivos `.csv`.
- Botão para salvar print da tela.
- Mensagens informativas:
  - "Por favor aguarde! Os dados estão sendo extraídos..."
  - "Dados extraídos com sucesso!"
  - "Arquivos CSV salvos com sucesso!
  - "Print salvo com sucesso."

## Como Utilizar

### 1. Instale as bibliotecas necessárias:
```bash
pip install requests beautifulsoup pandas customtkinter pyautogui
```

### 2. Execute a interface 
```bash
python interface.py
```

