from pynput.mouse import Listener
import keyboard
import sys

def verificar_cancelamento():
    if keyboard.is_pressed('esc'):
        print("Script cancelado pelo usuário.")
        sys.exit()  # Encerra o script imediatamente

def on_click(x, y, button, pressed):
    if pressed:
        # print(f"Mouse clicked at ({x}, {y})")
        print(f"pyautogui.click({x}, {y}, duration=0.15)")
        verificar_cancelamento()

# Iniciando o listener para capturar o clique do mouse.
with Listener(on_click=on_click) as listener:
    listener.join()


# $ pip install mouseinfo
# $ python
# >>> from mouseinfo import mouseInfo
# >>> mouseInfo()
