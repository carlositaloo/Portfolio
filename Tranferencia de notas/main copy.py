import subprocess
import pyautogui
import os
import pystray
from PIL import Image
from pynput.keyboard import Key, Listener

os.system('cls')
print("Em execução...")
img_icon = Image.open("icon.png")
rodada = 0
processo = None

def sair_do_programa():
    global processo  # Declare processo como global
    if processo:
        print("Encerrando o programa...")
        processo.kill()
    icon.stop()
    os._exit(0)

def executar_meu_script():
    global processo  # Declare processo como global
    try:
        processo = subprocess.Popen(["python", "script.py"])
        processo.wait()  # Aguarda até que o processo termine
    except Exception as e:
        print(f"Erro ao executar o script: {e}")

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

icon = pystray.Icon("Copy nota", img_icon, menu=pystray.Menu(
    pystray.MenuItem("Quit", sair_do_programa)
))

# Configurar o listener de teclado
with Listener(on_press=cola_nota) as listener:
    icon.run()
    listener.join()

