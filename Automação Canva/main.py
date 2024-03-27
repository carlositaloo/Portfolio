import os
import pandas as pd
import pyautogui
import pyperclip
from pynput import keyboard
from time import sleep

os.system('cls')

path_clone = 'img/clone.png'
path_texto = 'img/texto.png'
arquivo_excel = 'arquivo.xlsx'
litas_nomes = []

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
    # Pegar a primeira coluna (assumindo que é a coluna 0)
    nomes = df.iloc[:, 4]
    # Remover linhas vazias e parar se encontrar alguma
    for nome in nomes:
        if pd.isna(nome):
            print("Linha vazia encontrada, interrompendo a leitura.")
            break
        litas_nomes.append(nome)

    return litas_nomes

def criar_designs(nomes):
    if execucao_cancelada:
        return
    
    pyautogui.click(697,880)
    pyautogui.PAUSE = 0.4
    nomes.sort(key=str.upper)
    for indice, nome in enumerate(reversed(nomes), start=1):
        if execucao_cancelada:
            break
        print(f"{indice}. {nome}")
        pyperclip.copy(nome)
        
        # pyautogui.click(452,191)
        pyautogui.press('PageUp', presses=3)
        
        path = list(pyautogui.locateAllOnScreen(path_clone, confidence=0.9))
        x, y = pyautogui.center(path[0])
        pyautogui.click(x, y)
        
        pyautogui.click(452, 191)
        pyautogui.press('PageUp', presses=3)
        
        path = list(pyautogui.locateAllOnScreen(path_texto, confidence=0.9))
        x, y = pyautogui.center(path[1])
        pyautogui.doubleClick(x,y)
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('ctrl', 'v')
    pyautogui.click(1404,597)


# Executando o script e imprimindo os nomes
ler_nomes_excel(arquivo_excel)
criar_designs(litas_nomes)
