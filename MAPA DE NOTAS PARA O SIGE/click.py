from pynput.mouse import Listener
import pyautogui

def on_click(x, y, button, pressed):
    if pressed:
        print(f"Mouse clicked at ({x}, {y})")
        # Aqui você pode adicionar o código para usar pyautogui e realizar ações com essas coordenadas.
        # Por exemplo, para mover o mouse para essa posição: pyautogui.moveTo(x, y)
        # Para clicar nessa posição: pyautogui.click(x, y)
        
        # Para parar o listener depois do primeiro clique.
        return False

# Iniciando o listener para capturar o clique do mouse.
with Listener(on_click=on_click) as listener:
    listener.join()
