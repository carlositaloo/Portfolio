from pynput.mouse import Listener
from pynput import keyboard as pynput_keyboard
import sys
import time

# Variáveis para armazenar tempos
ultimo_evento = None
cancelado = False

def on_key_press(key):
    global ultimo_evento, cancelado
    
    if cancelado:
        return False
    
    try:
        # Tecla ESC para cancelar
        if key == pynput_keyboard.Key.esc:
            print("\nScript cancelado pelo usuário.")
            cancelado = True
            return False
        
        tempo_atual = time.time()
        
        # Calcula tempo desde último evento (se houver)
        if ultimo_evento is not None:
            tempo_decorrido = tempo_atual - ultimo_evento
            print(f"time.sleep(timeset)")
        
        # Tratamento para teclas especiais
        if key == pynput_keyboard.Key.enter:
            print("pyautogui.press('enter')")
        elif key == pynput_keyboard.Key.tab:
            print("pyautogui.press('tab')")
        elif key == pynput_keyboard.Key.space:
            print("pyautogui.press('space')")
        elif key == pynput_keyboard.Key.backspace:
            print("pyautogui.press('backspace')")
        elif key == pynput_keyboard.Key.delete:
            print("pyautogui.press('delete')")
        elif key == pynput_keyboard.Key.shift:
            print("pyautogui.press('shift')")
        elif key == pynput_keyboard.Key.ctrl_l or key == pynput_keyboard.Key.ctrl_r:
            print("pyautogui.press('ctrl')")
        elif key == pynput_keyboard.Key.alt_l or key == pynput_keyboard.Key.alt_r:
            print("pyautogui.press('alt')")
        elif key == pynput_keyboard.Key.up:
            print("pyautogui.press('up')")
        elif key == pynput_keyboard.Key.down:
            print("pyautogui.press('down')")
        elif key == pynput_keyboard.Key.left:
            print("pyautogui.press('left')")
        elif key == pynput_keyboard.Key.right:
            print("pyautogui.press('right')")
        elif key == pynput_keyboard.Key.home:
            print("pyautogui.press('home')")
        elif key == pynput_keyboard.Key.end:
            print("pyautogui.press('end')")
        elif key == pynput_keyboard.Key.page_up:
            print("pyautogui.press('pageup')")
        elif key == pynput_keyboard.Key.page_down:
            print("pyautogui.press('pagedown')")
        elif hasattr(key, 'name') and key.name.startswith('f'):
            # Teclas de função F1, F2, etc.
            print(f"pyautogui.press('{key.name}')")
        else:
            # Tentativa de capturar outras teclas especiais
            key_name = str(key).replace('Key.', '').replace("'", "")
            if len(key_name) > 1:
                print(f"pyautogui.press('{key_name}')")
        
        # Atualiza o tempo do último evento
        ultimo_evento = tempo_atual
        
    except AttributeError:
        # Teclas normais (letras, números, símbolos)
        tempo_atual = time.time()
        
        if ultimo_evento is not None:
            tempo_decorrido = tempo_atual - ultimo_evento
            print(f"time.sleep(timeset)")
        
        # Remove as aspas simples da representação da tecla
        char = str(key).replace("'", "")
        print(f"pyautogui.press('{char}')")
        
        ultimo_evento = tempo_atual

def on_click(x, y, button, pressed):
    global ultimo_evento, cancelado
    
    if cancelado:
        return False
    
    if pressed:
        tempo_atual = time.time()
        
        # Se não é o primeiro evento, calcula o tempo decorrido
        if ultimo_evento is not None:
            tempo_decorrido = tempo_atual - ultimo_evento
            print(f"time.sleep(timeset)")
        
        # Identifica qual botão foi clicado
        if str(button) == "Button.left":
            print(f"pyautogui.click({x}, {y}, duration=0.15)")
        elif str(button) == "Button.right":
            print(f"pyautogui.rightClick({x}, {y}, duration=0.15)")
        elif str(button) == "Button.middle":
            print(f"pyautogui.middleClick({x}, {y}, duration=0.15)")
        
        # Atualiza o tempo do último evento
        ultimo_evento = tempo_atual

print("🖱️  Iniciando captura de mouse e teclado...")
print("⌨️  Pressione ESC para cancelar")
print("📝 Comandos serão exibidos no formato PyAutoGUI")
print("=" * 60)

# Iniciando listeners para mouse e teclado
try:
    with pynput_keyboard.Listener(on_press=on_key_press) as key_listener:
        with Listener(on_click=on_click) as mouse_listener:
            key_listener.join()  # Espera até ESC ser pressionado
            mouse_listener.stop()  # Para o listener do mouse quando ESC é pressionado
except KeyboardInterrupt:
    print("\nScript interrompido via Ctrl+C")

print("✅ Script finalizado.")