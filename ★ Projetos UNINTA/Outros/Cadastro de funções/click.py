from pynput.mouse import Listener

def on_click(x, y, button, pressed):
    if pressed:
        print(f"Mouse clicked at ({x}, {y})")
        
        return False

# Iniciando o listener para capturar o clique do mouse.
with Listener(on_click=on_click) as listener:
    listener.join()


# $ pip install mouseinfo
# $ python
# >>> from mouseinfo import mouseInfo
# >>> mouseInfo()
