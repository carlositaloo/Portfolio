import os
import pandas as pd
import pyautogui
import pyperclip
from pynput import keyboard
from time import sleep

# Configurações
fazer_clone = False     # Se deve criar clone
num_textos = 1          # Quantos textos vai modificar
num_coluna = 0          # Coluna inicial no Excel '0 = Default'
path_textos = ['img/texto.png', 'img/texto1.png', 'img/texto2.png', 'img/texto3.png']

navegadorxy = (720, 883)  # Coordenadas do botão do navegador
foralayout = (1403, 187)  # Coordenadas fora do layout

path_clone = 'img/clone.png'
arquivo_excel = 'arquivo.xlsx'
execucao_cancelada = False  # Variável global para controlar a execução do código

# Limpa o terminal
os.system('cls')

# Inicializa listas para armazenar os nomes
listas_colunas = [[] for _ in range(num_textos + 1)]

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
    """Lê os nomes do arquivo Excel e armazena em listas."""
    df = pd.read_excel(arquivo, header=None)
    for i in range(num_textos):
        coluna = df.iloc[:, i + num_coluna]
        for nome in coluna:
            if pd.isna(nome):
                print("Linha vazia encontrada, interrompendo a leitura.")
                break
            listas_colunas[i].append(nome)
    return listas_colunas

def clicar_botao_clone():
    """Clica no botão de clone."""
    pyautogui.click(foralayout)
    pyautogui.press('PageUp', presses=3)
    sleep(0.5)
    path = list(pyautogui.locateAllOnScreen(path_clone, confidence=0.9))
    if path:
        x, y = pyautogui.center(path[0])
        pyautogui.click(x, y)
        sleep(1)

def processar_textos(listas_colunas):
    """Itera sobre os textos e realiza as modificações necessárias."""
    pyautogui.click(navegadorxy)
    pyautogui.PAUSE = 0.4
    
    max_length = max(len(lista) for lista in listas_colunas)
    
    for i in range(max_length):
        if execucao_cancelada:
            break

        if fazer_clone:
            clicar_botao_clone()

        for j, lista in enumerate(listas_colunas):
            if i < len(lista):
                texto = lista[i]
                pyperclip.copy(texto)
                path = list(pyautogui.locateAllOnScreen(path_textos[j + num_coluna], confidence=0.9))
                if path:
                    x, y = pyautogui.center(path[0])
                    pyautogui.doubleClick(x, y)
                    pyautogui.hotkey('ctrl', 'a')
                    pyautogui.hotkey('ctrl', 'v')
                    pyautogui.click(foralayout)
        
        if execucao_cancelada:
            break
        
        print(f"{i + 1}. {', '.join(listas_colunas[j][i] for j in range(len(listas_colunas)) if i < len(listas_colunas[j]))}")
        
        if not fazer_clone:
            pyautogui.press('PageDown', presses=1)
            sleep(0.5)

    pyautogui.click(foralayout)

# Executando o script
ler_nomes_excel(arquivo_excel)
processar_textos(listas_colunas)
