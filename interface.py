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
from quotes import analisa_citacoes

# Executa a raspagem e limpa toda área de texto da interface
def executarRaspagem():
    resultados.delete('0.0', 'end')
    citacoes = analisa_citacoes()
    
    for c in citacoes:
        texto = f"Autor: {c['Nome do autor']}\nFrase: {c['Citação']}\nTags: {', '.join(c['Tags'])}\n---\n"
        resultados.insert("end", texto)

# Executa em segundo plano para não travar a interface
def chamar_thread():
    threading.Thread(target=executarRaspagem).start()

# Configurando a aparência

ctk.set_appearance_mode('dark')

# Criando janela da interface
interface = ctk.CTk()
interface.title('Raspagem de Dados - Quotes to Scrape')
interface.geometry('700x500')

# Botão para excutar a raspagem do programa Quetos
botao_execucao = ctk.CTkButton(interface, text='Excutar', command=chamar_thread)
botao_execucao.pack(pady=10)

# Área de texto, onde os dados serão exibidos
resultados = ctk.CTkTextbox(interface, width=600, height=300)
resultados.pack(pady=20)

interface.mainloop()


