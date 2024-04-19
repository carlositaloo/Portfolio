import os
import pandas as pd
import pyautogui
import pyperclip
from pynput import keyboard
from time import sleep

os.system('cls')

# Digite 1 para criar designs a partir de um design já existente ou 
# 2 para alterar o texto de designs já existentes
tipo_design = 2

path_clone = 'img/clone.png'
path_texto = 'img/texto.png'
path_texto1 = 'img/texto1.png'
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
    df = pd.read_excel(arquivo, header=None)    # Ler o arquivo Excel
    # Pegar a primeira coluna (assumindo que é a coluna 0)
    nomes = df.iloc[:, 0]   # Alterar o número da coluna se necessário
    # Remover linhas vazias e parar se encontrar alguma
    for nome in nomes:  
        if pd.isna(nome):   # Se a linha estiver vazia
            print("Linha vazia encontrada, interrompendo a leitura.")
            break
        litas_nomes.append(nome)

    return litas_nomes

    # Essa função cria os designs a partir de um desing já existente, criando clones e alterando o texto
def criar_designs(nomes):
    if execucao_cancelada:  # Verificar se a tecla ESC foi pressionada e cancelar a execução
        return
    
    pyautogui.click(697,880)    # Clicar no botão do navegador *Defina as coordenadas*
    pyautogui.PAUSE = 0.4
    nomes.sort(key=str.upper)   # Ordenar os nomes em ordem alfabética
    for indice, nome in enumerate(reversed(nomes), start=1):    # Iterar sobre os nomes
        if execucao_cancelada:  # Verificar se a tecla ESC foi pressionada e cancelar a execução
            break
        print(f"{indice}. {nome}")
        pyperclip.copy(nome)
        
        # pyautogui.click(452,191)
        pyautogui.press('PageUp', presses=3)    # Subir a página
        
        path = list(pyautogui.locateAllOnScreen(path_clone, confidence=0.9))    # Procurar o botão de clone
        x, y = pyautogui.center(path[0])    # Pegar o centro do botão e armazena em x e y
        pyautogui.click(x, y)   # Clicar no botão de clone
        
        pyautogui.click(452, 191)   # Clicar fora do layout
        pyautogui.press('PageUp', presses=3)    # Subir a página
        
        path = list(pyautogui.locateAllOnScreen(path_texto, confidence=0.9))    # Procurar o campo de texto
        # Defina o índice do campo de texto* 0 primeiro campo, 1 segundo campo...
        x, y = pyautogui.center(path[1])    # Pegar o centro do campo de texto e armazena em x e y
        pyautogui.doubleClick(x,y)  # Clicar duas vezes no campo de texto
        pyautogui.hotkey('ctrl', 'a')   # Selecionar o texto
        pyautogui.hotkey('ctrl', 'v')   # Colar o texto
    pyautogui.click(1404,597)   # Clicar fora do layout

    # Essa função apenas altera o texto dos designs já existentes
def designs_existentes(nomes):
    if execucao_cancelada:  # Verificar se a tecla ESC foi pressionada e cancelar a execução
        return
    
    pyautogui.click(697,880)    # Clicar no botão do navegador *Defina as coordenadas*
    pyautogui.PAUSE = 0.4
    for indice, nome in enumerate(nomes, start=1):    # Iterar sobre os nomes
        if execucao_cancelada:  # Verificar se a tecla ESC foi pressionada e cancelar a execução
            break
        print(f"{indice}. {nome}")
        pyperclip.copy(nome)
        
        path = list(pyautogui.locateAllOnScreen(path_texto1, confidence=0.9))    # Procurar o campo de texto
        # Defina o índice do campo de texto* 0 primeiro campo, 1 segundo campo...
        x, y = pyautogui.center(path[0])    # Pegar o centro do campo de texto e armazena em x e y 
        pyautogui.doubleClick(x,y)  # Clicar duas vezes no campo de texto
        pyautogui.hotkey('ctrl', 'a')   # Selecionar o texto
        pyautogui.hotkey('ctrl', 'v')   # Colar o texto
        pyautogui.click(452, 191)   # Clicar fora do layout
        
        pyautogui.press('PageDown', presses=1)    # Vai para o próximo design
    pyautogui.click(1404,597)   # Clicar fora do layout

# Executando o script e imprimindo os nomes
ler_nomes_excel(arquivo_excel)
if tipo_design == 1:
    criar_designs(litas_nomes)
elif tipo_design == 2:
    designs_existentes(litas_nomes)
