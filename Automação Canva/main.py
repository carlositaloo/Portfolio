import os
import pandas as pd
import pyautogui
import pyperclip
from pynput import keyboard
from time import sleep

os.system('cls')

# Configurações
fazer_clone = False     # Se deve criar clone
num_textos = 1          # Quantos textos vai modificar
num_coluna = 0          # 0 = default
path_textos = ['img/texto.png', 'img/texto1.png', 'img/texto2.png', 'img/texto3.png' ]

navegadorxy = 720, 883  # Coordenadas do botão do navegador
foralayout = 1403, 187  # Coordenadas fora do layout

path_clone = 'img/clone.png'
arquivo_excel = 'arquivo.xlsx'


# Armazenar os nomes em uma lista
listas_colunas = [[] for _ in range(num_textos + 1)]
# Variável global para controlar a execução do código
execucao_cancelada = False


def on_press(key):
    global execucao_cancelada
    if key == keyboard.Key.esc:
        print("Execução cancelada.")
        execucao_cancelada = True
        return False  # Para a execução do listener


# Criar um listener para a tecla "Esc"
listener = keyboard.Listener(on_press=on_press)
listener.start()


def ler_nomes_excel(arquivo):
    # Ler o arquivo Excel
    df = pd.read_excel(arquivo, header=None)
    # Pegar as colunas necessárias
    for i in range(num_textos):
        coluna = df.iloc[:, i+num_coluna]
        for nome in coluna:
            if pd.isna(nome):   # Se a linha estiver vazia
                print("Linha vazia encontrada, interrompendo a leitura.")
                break
            listas_colunas[i].append(nome)
    return listas_colunas

def fazer_designs(listas_colunas):
    if execucao_cancelada:  # Verificar se a tecla ESC foi pressionada e cancelar a execução
        return

    # Clicar no botão do navegador *Defina as coordenadas*
    pyautogui.click(navegadorxy)  # Clicar no botão do navegador
    pyautogui.PAUSE = 0.4
    
    # Iterar sobre a colunas
    max_length = max(len(lista) for lista in listas_colunas)

    for i in range(max_length):
        items = []
        if fazer_clone == True:
            pyautogui.click(foralayout)
            pyautogui.press('PageUp', presses=3)    # Subir a página
            sleep(0.5)
            path = list(pyautogui.locateAllOnScreen(path_clone, confidence=0.9))
            # Pegar o centro do botão CLONE e armazena em x e y
            x, y = pyautogui.center(path[0])
            pyautogui.click(x, y)   # Clicar no botão de clone
            sleep(1)
            
        for j, lista in enumerate(listas_colunas):
            if i < len(lista):
                items.append(f"{lista[i]}")
                pyperclip.copy(lista[i])
                
                if execucao_cancelada:  # Verificar se a tecla ESC foi pressionada e cancelar a execução
                    break
                
                # Procurar o campo de texto
                path = list(pyautogui.locateAllOnScreen(path_textos[j+num_coluna], confidence=0.9))
                if path:
                    # Pegar o centro do campo de texto e armazena em x e y
                    x, y = pyautogui.center(path[0])
                    pyautogui.doubleClick(x, y)  # Clicar duas vezes no campo de texto
                    pyautogui.hotkey('ctrl', 'a')   # Selecionar o texto
                    pyautogui.hotkey('ctrl', 'v')   # Colar o texto
                    pyautogui.click(foralayout)   # Clicar fora do layout
        print(f"{i + 1}. {', '.join(items)}")
        if execucao_cancelada:  # Verificar se a tecla ESC foi pressionada e cancelar a execução
            break
        if fazer_clone == False:
            pyautogui.press('PageDown', presses=1)    # Vai para o próximo design
            sleep(0.5)
    pyautogui.click(foralayout)   # Clicar fora do layout


# Executando o script e imprimindo os nomes
ler_nomes_excel(arquivo_excel)
fazer_designs(listas_colunas)
