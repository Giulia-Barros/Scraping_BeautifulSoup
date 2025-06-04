# /***********************************************************************************
# |----------------------------------------------------------------------------------|
# |* Programa   | Interface                                                         *|
# |----------------------------------------------------------------------------------|
# |* Autor      |  Giulia Barros                                                    *|
# |----------------------------------------------------------------------------------|
# |* Utilização | Execução e visualização do programa Quotes                        *|
# |----------------------------------------------------------------------------------|
# |* Descricao  | Interface para executar e visualizar os resultados do programa    *|
# |             | Quetos.                                                            |
# |----------------------------------------------------------------------------------|
import customtkinter as ctk
import threading
import pandas as pd
import pyautogui
from quotes import analisa_citacoes


# Configuração da aparência
ctk.set_appearance_mode('dark')
interface = ctk.CTk()
interface.title('Raspagem de Dados - Quotes to Scrape')
interface.geometry('700x700')

# Função para tirar o print da tela
def printTela():
    printt = pyautogui.screenshot()
    printt.save("print_.png")
    aviso.configure(text="Print salvo com sucesso.")

# Executa a raspagem e atualiza as áreas de texto
def executarRaspagem():
    aviso.configure(text="Por favor aguarde! Os dados estão sendo extraídos...")

    resultadosCitacoes.delete('0.0', 'end')
    resultadosAutores.delete('0.0', 'end')

    citacoes, autores = analisa_citacoes()

    # Percorre as listas das informações das Citações
    for c in citacoes:
        texto = f"Autor: {c['Nome do autor']}\nFrase: {c['Citação']}\nTags: {', '.join(c['Tags'])}\n---\n"
        resultadosCitacoes.insert("end", texto)

    # Percorre as listas das informações dos Autores
    for a in autores:
        texto = (
            f"Autor: {a['Nome completo']}\n"
            f"Nascimento: {a['Data de nascimento']}\n"
            f"Local: {a['Local de nascimento']}\n"
            f"Sobre o autor: {a['Descrição']}\n---\n"
        )
        resultadosAutores.insert("end", texto)

    # Salva os dados na interface para exportação
    interface.citacoes_data = citacoes
    interface.autores_data = autores

    aviso.configure(text="Dados extraídos com sucesso!")

# Exporta para CSV
def exportarCSV():
    citacoes_csv = getattr(interface, "citacoes_data", [])
    autores_csv = getattr(interface, "autores_data", [])

    if citacoes_csv and autores_csv:
        pd.DataFrame(citacoes_csv).to_csv('citacoes.csv', index=False)
        pd.DataFrame(autores_csv).to_csv('autores.csv', index=False)
        aviso.configure(text="Arquivos CSV salvos com sucesso!")
    else:
        aviso.configure(text="Nenhum dado para exportar. Execute a raspagem primeiro.")

# Executa em segundo plano
def chamarThread():
    threading.Thread(target=executarRaspagem).start()

# Botão para executar
botao_execucao = ctk.CTkButton(interface, text='Executar Raspagem', command=chamarThread)
botao_execucao.pack(pady=10)

# Botão para exportar
botao_exportar = ctk.CTkButton(interface, text='Exportar para CSV', command=exportarCSV)
botao_exportar.pack(pady=5)

# Botão para tirar screenshot
botao_screenshot = ctk.CTkButton(interface, text='Salvar Print', command=printTela)
botao_screenshot.pack(pady=10)

# Avisos
aviso = ctk.CTkLabel(interface, text="")
aviso.pack(pady=5)

# Área de texto das Citações
resultadosCitacoes = ctk.CTkTextbox(interface, width=600, height=250)
resultadosCitacoes.pack(pady=10)

# Área de texto dos Autores
resultadosAutores = ctk.CTkTextbox(interface, width=600, height=250)
resultadosAutores.pack(pady=10)

# Loop principal
interface.mainloop()