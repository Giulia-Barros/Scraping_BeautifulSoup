import customtkinter as ctk
import threading
from quotes import analisa_citacoes


def executarRaspagem():
    resultados.delete('0.0', 'end')
    citacoes = analisa_citacoes()
    
    for c in citacoes:
        texto = f"Autor: {c['Nome do autor']}\nFrase: {c['Citação']}\nTags: {', '.join(c['Tags'])}\n---\n"
        resultados.insert("end", texto)

def chamar_thread():
    threading.Thread(target=executarRaspagem).start()

#Configurando a aparência
ctk.set_appearance_mode('dark')
#Criando Janela
interface = ctk.CTk()
interface.title('Raspagem de Dados - Quotes to Scrape')
interface.geometry('700x500')

#Criando Botao
botao_execucao = ctk.CTkButton(interface, text='Excutar', command=chamar_thread)
botao_execucao.pack(pady=10)

#Criando Área de Texto
resultados = ctk.CTkTextbox(interface, width=600, height=300)
resultados.pack(pady=20)

interface.mainloop()


