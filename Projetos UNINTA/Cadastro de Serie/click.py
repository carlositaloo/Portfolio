from pynput.mouse import Listener
from pynput import keyboard as pynput_keyboard
import sys
import time

# Variável para armazenar o tempo do último click
ultimo_click = None
cancelado = False

# SOLUÇÃO 1: Usando pynput para teclado também (RECOMENDADA)
def on_key_press(key):
    global cancelado
    try:
        if key == pynput_keyboard.Key.esc:
            print("\nScript cancelado pelo usuário.")
            cancelado = True
            return False  # Para o listener do teclado
    except AttributeError:
        pass

def on_click(x, y, button, pressed):
    global ultimo_click, cancelado
    
    if cancelado:
        return False  # Para o listener do mouse
    
    if pressed:
        tempo_atual = time.time()
        
        # Se não é o primeiro click, calcula o tempo decorrido
        if ultimo_click is not None:
            tempo_decorrido = tempo_atual - ultimo_click
            print(f"time.sleep({tempo_decorrido:.2f})")
            # print(f"time.sleep(timeset)")
        
        # Exibe o comando do click
        print(f"pyautogui.click({x}, {y}, duration=0.15)")
        
        # Atualiza o tempo do último click
        ultimo_click = tempo_atual

print("Iniciando captura de clicks e tempos...")
print("Pressione ESC para cancelar")
print("=" * 50)

# Iniciando listeners para mouse e teclado
try:
    with pynput_keyboard.Listener(on_press=on_key_press) as key_listener:
        with Listener(on_click=on_click) as mouse_listener:
            key_listener.join()  # Espera até ESC ser pressionado
            mouse_listener.stop()  # Para o listener do mouse quando ESC é pressionado
except KeyboardInterrupt:
    print("\nScript interrompido via Ctrl+C")

print("Script finalizado.")