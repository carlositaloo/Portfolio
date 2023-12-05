# python
# from mouseinfo import mouseInfo
# mouseInfo()
# F6

import os
import pandas as pd
import pyautogui
import pyperclip

os.system('cls')

path_clone = 'img/clone.png'
arquivo_excel = 'arquivo.xlsx'
litas_nomes = []

def ler_nomes_excel(arquivo):
    # Ler o arquivo Excel
    df = pd.read_excel(arquivo, header=None)
    # Pegar a primeira coluna (assumindo que é a coluna 0)
    nomes = df.iloc[:, 3]
    # Remover linhas vazias e parar se encontrar alguma
    for nome in nomes:
        if pd.isna(nome):
            print("Linha vazia encontrada, interrompendo a leitura.")
            break
        litas_nomes.append(nome)

    return litas_nomes

def criar_designs(nomes):
    pyautogui.click(661,880)
    pyautogui.PAUSE = 0.4
    nomes.sort(key=str.upper)
    for indice, nome in enumerate(reversed(nomes), start=1):
        print(f"{indice}. {nome}")
        pyperclip.copy(nome)
        
        pyautogui.click(1404,597)
        pyautogui.press('PageUp', presses=3)
        
        path = list(pyautogui.locateAllOnScreen(path_clone, confidence=0.9))
        x, y = pyautogui.center(path[0])
        pyautogui.click(x, y)
        
        # pyautogui.doubleClick(931,321)
        pyautogui.doubleClick(941,623)
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('ctrl', 'v')
    pyautogui.click(1404,597)


# Executando o script e imprimindo os nomes
ler_nomes_excel(arquivo_excel)
criar_designs(litas_nomes)