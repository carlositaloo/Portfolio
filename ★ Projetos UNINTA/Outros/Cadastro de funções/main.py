import pandas as pd
import pyautogui
import keyboard
import pyperclip
import time
import sys

# Função para verificar se a tecla ESC foi pressionada
def verificar_cancelamento():
    if keyboard.is_pressed('esc'):
        print("Script cancelado pelo usuário.")
        sys.exit()  # Encerra o script imediatamente

# Defina o índice a partir do qual deseja começar
indice_inicio = 0  # Altere esse valor para o ponto onde deseja reiniciar
timeset = 0.2  # Tempo de espera entre ações

# Carrega a planilha Excel
df = pd.read_excel('UNCOES-RM-AIAMIS modificado.xlsx')
# Garante que a coluna 'Nome' existe e remove valores nulos
lista_nomes = df['Descricao'].dropna().tolist()  # Ignora células vazias

# Mensagem só aparece se começar do índice 0
if indice_inicio == 0:
    print(f"\n\nColunas encontradas:\n{list(df.columns)}\n")
    print("Iniciando do índice 0. Pressione ESC para cancelar.\n")

# Validações sempre executam
if indice_inicio < 0:
    print("Erro: Índice de início não pode ser negativo.")
    sys.exit()

if indice_inicio >= len(lista_nomes):
    print(f"Erro: Índice {indice_inicio} é maior que total de itens ({len(lista_nomes)})")
    sys.exit()

# pyautogui.hotkey("alt", "tab")  # muda de janela
# time.sleep(0.5)

# Percorre a lista a partir do índice desejado
for i in range(indice_inicio, len(lista_nomes)):
    nome = lista_nomes[i]

    verificar_cancelamento()
    pyperclip.copy(str(nome))

    verificar_cancelamento()
    pyautogui.click(14, 200, duration=0.25)  # click em Adicionar
    time.sleep(timeset)

    verificar_cancelamento()
    pyautogui.click(1088, 463, duration=0.25)  # click na área do Nome
    time.sleep(timeset)

    verificar_cancelamento()
    print(f"[{i+1}] - {nome}")
    pyautogui.hotkey("ctrl", "v")  # Cola
    time.sleep(timeset)

    verificar_cancelamento()
    pyautogui.click(1066, 722, duration=0.25)  # click em Confirmar
    time.sleep(timeset)
