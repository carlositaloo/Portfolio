import pyautogui
import pyperclip
import pandas as pd
from pynput import keyboard
from time import sleep

# Configurações
navegadorxy = (690, 885)  # Coordenadas do botão do navegador
layoutxy = (590, 670)    # Coordenadas do layout para o clique inicial
quantidade_itens = 28     # Quantidade de itens a preencher
linha_inicial = 56        # Linha inicial de leitura no Excel (0 = primeira linha)
arquivo_excel = 'arquivo1.xlsx'  # Nome do arquivo Excel

execucao_cancelada = False  # Variável global para controlar a execução do código

# Função para capturar a tecla ESC e interromper o script
def on_press(key):
    global execucao_cancelada
    if key == keyboard.Key.esc:
        print("Execução cancelada pelo usuário.")
        execucao_cancelada = True
        return False  # Para o listener

# Inicia o listener para capturar a tecla ESC
listener = keyboard.Listener(on_press=on_press)
listener.start()

# Ler arquivo Excel (a partir da linha inicial até a quantidade necessária)
def ler_nomes_excel(arquivo, linha_inicial, quantidade_itens):
    df = pd.read_excel(arquivo, header=None)
    nomes = df.iloc[linha_inicial:, 0].dropna().tolist()  # Pega da linha inicial em diante
    return nomes[:quantidade_itens]  # Retorna apenas a quantidade especificada

# Lista de nomes do Excel
nomes = ler_nomes_excel(arquivo_excel, linha_inicial, quantidade_itens)

# Automação
def preencher_campos(nomes):
    # Clicar no navegador
    pyautogui.click(navegadorxy)
    sleep(1)

    # Dois cliques no layout
    pyautogui.doubleClick(layoutxy)
    sleep(1)

    # Preencher os campos
    for nome in nomes:
        if execucao_cancelada:  # Verifica se a execução foi cancelada
            print("Execução interrompida.")
            break

        pyperclip.copy(nome)  # Copiar o nome para a área de transferência
        pyautogui.hotkey('ctrl', 'a')  # Selecionar tudo
        pyautogui.hotkey('ctrl', 'v')  # Colar o nome
        pyautogui.press('tab')  # Passar para o próximo campo
        sleep(0.5)  # Pequeno delay para estabilidade

# Executa o preenchimento
preencher_campos(nomes)
