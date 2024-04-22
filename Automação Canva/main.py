import os
import pandas as pd
import pyautogui
import pyperclip
from pynput import keyboard
from time import sleep

os.system('cls')

# Configurações
# 1 para criar designs a partir de um design já existente
# 2 para alterar o texto de designs já existentes
# 3 para alterar o texto de designs já existentes com dois textos
tipo_design = 3
navegadorxy = 722, 882  # Coordenadas do botão do navegador
foralayout = 1403, 187  # Coordenadas fora do layout

path_clone = 'img/clone.png'
path_texto = 'img/texto.png'
path_texto1 = 'img/texto1.png'
arquivo_excel = 'arquivo.xlsx'

# Armazenar os nomes em uma lista
lista_coluna1 = []
lista_coluna2 = []

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
    coluna1 = df.iloc[:, 0]   # Alterar o número da coluna se necessário
    if tipo_design == 3:
        coluna2 = df.iloc[:, 1]   # Alterar o número da coluna se necessário
        for nome2 in coluna2:
            lista_coluna2.append(nome2)

    for nome1 in coluna1:
        if pd.isna(nome1):   # Se a linha estiver vazia
            print("Linha vazia encontrada, interrompendo a leitura.")
            break
        lista_coluna1.append(nome1)

    return lista_coluna1, lista_coluna2

    # Essa função cria os designs a partir de um desing já existente, criando clones e alterando o texto


def criar_designs(coluna1):
    if execucao_cancelada:  # Verificar se a tecla ESC foi pressionada e cancelar a execução
        return

    # Clicar no botão do navegador *Defina as coordenadas*
    pyautogui.click(navegadorxy)  # Clicar no botão do navegador
    pyautogui.PAUSE = 0.4
    coluna1.sort(key=str.upper)   # Ordenar a coluna1 em ordem alfabética
    # Iterar sobre a coluna1
    for indice, nome in enumerate(reversed(coluna1), start=1):
        if execucao_cancelada:  # Verificar se a tecla ESC foi pressionada e cancelar a execução
            break
        print(f"{indice}. {nome}")
        pyperclip.copy(nome)

        path = list(pyautogui.locateAllOnScreen(path_clone, confidence=0.9))
        # Pegar o centro do botão e armazena em x e y
        x, y = pyautogui.center(path[0])
        pyautogui.click(x, y)   # Clicar no botão de clone

        pyautogui.click(foralayout)   # Clicar fora do layout
        pyautogui.press('PageUp', presses=3)    # Subir a página

        # Procurar o campo de texto
        path = list(pyautogui.locateAllOnScreen(path_texto, confidence=0.9))
        # Defina o índice do campo de texto* 0 primeiro campo, 1 segundo campo...
        # Pegar o centro do campo de texto e armazena em x e y
        x, y = pyautogui.center(path[1])
        pyautogui.doubleClick(x, y)  # Clicar duas vezes no campo de texto
        pyautogui.hotkey('ctrl', 'a')   # Selecionar o texto
        pyautogui.hotkey('ctrl', 'v')   # Colar o texto
    pyautogui.click(foralayout)   # Clicar fora do layout

    # Essa função apenas altera o texto dos designs já existentes


def designs_existentes(coluna1, coluna2):
    if execucao_cancelada:  # Verificar se a tecla ESC foi pressionada e cancelar a execução
        return

    # Clicar no botão do navegador *Defina as coordenadas*
    pyautogui.click(navegadorxy)  # Clicar no botão do navegador
    pyautogui.PAUSE = 0.4
    # Iterar sobre a coluna1
    # for indice, (nome1, nome2) in enumerate(zip(coluna1, coluna2 or []), start=1):
    for indice, nome1 in enumerate(coluna1, start=1):
        if tipo_design == 3:
            nome2 = coluna2[indice - 1]
        else:
            nome2 = ''

        if execucao_cancelada:  # Verificar se a tecla ESC foi pressionada e cancelar a execução
            break
        print(f"{indice}. {nome1} {nome2}")
        pyperclip.copy(nome1)

        # Procurar o campo de texto
        path = list(pyautogui.locateAllOnScreen(path_texto1, confidence=0.9))
        # Defina o índice do campo de texto* 0 primeiro campo, 1 segundo campo...
        # Pegar o centro do campo de texto e armazena em x e y
        x, y = pyautogui.center(path[0])
        pyautogui.doubleClick(x, y)  # Clicar duas vezes no campo de texto
        pyautogui.hotkey('ctrl', 'a')   # Selecionar o texto
        pyautogui.hotkey('ctrl', 'v')   # Colar o texto
        pyautogui.click(foralayout)   # Clicar fora do layout

        if tipo_design == 3:
            pyperclip.copy(nome2)
            # Procurar o campo de texto
            path = list(pyautogui.locateAllOnScreen(
                path_texto1, confidence=0.9))
            # Defina o índice do campo de texto* 0 primeiro campo, 1 segundo campo...
            # Pegar o centro do campo de texto e armazena em x e y
            x, y = pyautogui.center(path[0])
            pyautogui.doubleClick(x, y)  # Clicar duas vezes no campo de texto
            pyautogui.hotkey('ctrl', 'a')   # Selecionar o texto
            pyautogui.hotkey('ctrl', 'v')   # Colar o texto
            pyautogui.click(foralayout)   # Clicar fora do layout

        pyautogui.press('PageDown', presses=1)    # Vai para o próximo design
    pyautogui.click(foralayout)   # Clicar fora do layout


# Executando o script e imprimindo os nomes
ler_nomes_excel(arquivo_excel)

if tipo_design == 1:
    criar_designs(lista_coluna1)
elif tipo_design == 2:
    designs_existentes(lista_coluna1, lista_coluna2)
elif tipo_design == 3:
    designs_existentes(lista_coluna1, lista_coluna2)
