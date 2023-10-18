import subprocess
import sys
import pyautogui
import os
from pynput.keyboard import Key, Listener

print("Em execução...")

# Defina a função que será executada quando a tecla F8 for pressionada
def executar_meu_script():
    try:
        # Substitua "caminho_para_seu_script.py" pelo caminho real do seu script
        processo = subprocess.Popen(["python", "script.py"])
        processo.wait()  # Aguarda até que o processo termine
    except Exception as e:
        print(f"Erro ao executar o script: {e}")

rodada = 1

# Função para verificar se a tecla F8 foi pressionada
def cola_nota(key):
    global rodada
    if key == Key.f8:
        os.system('cls')
        print("Executando o script...")
        executar_meu_script()
        rodada += 1
        for c in range(13 if rodada % 2 == 0 else 15):
            pyautogui.press('down')
    elif key == Key.esc:
        print("Script cancelado.")
        sys.exit(0)

# Configurar o listener de teclado 1 2 8
with Listener(on_press=cola_nota) as test:
    test.join()

