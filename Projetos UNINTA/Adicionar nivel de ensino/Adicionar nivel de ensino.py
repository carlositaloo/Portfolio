import pyautogui
import pyperclip
import time
import keyboard
import sys
import os

# ------------------------------
# Configurações iniciais
# ------------------------------
usuario = pyperclip.paste().strip()
nivelEnsino = "2"
timeset = 0.1
script_dir = os.path.dirname(os.path.abspath(__file__))

# ------------------------------
# Funções utilitárias
# ------------------------------

def verificar_cancelamento():
    """Cancela o script se ESC for pressionado"""
    try:
        if keyboard.is_pressed('esc'):
            print("Script cancelado pelo usuário.")
            time.sleep(0.1)  # evita múltiplas detecções
            if keyboard.is_pressed('esc'):
                sys.exit()
    except Exception:
        pass

def sleep_cancelamento(duration):
    """Sleep que verifica ESC a cada 0.1s"""
    elapsed = 0
    while elapsed < duration:
        verificar_cancelamento()
        sleep_time = min(0.1, duration - elapsed)
        time.sleep(sleep_time)
        elapsed += sleep_time

def aguardar_imagem(imagem_path, timeout=30, intervalo=0.1, confidence=0.8, continuar=False):
    """Aguarda uma imagem aparecer na tela"""
    caminho_completo = os.path.join(script_dir, imagem_path)
    inicio = time.time()
    while time.time() - inicio < timeout:
        verificar_cancelamento()
        try:
            posicao = pyautogui.locateOnScreen(caminho_completo, confidence=confidence)
            if posicao:
                return posicao
        except Exception as e:
            pass
        sleep_cancelamento(intervalo)
    if continuar:
        return None
    else:
        raise TimeoutError(f"Imagem {imagem_path} não encontrada em {timeout}s")

def clicar(posicao, duration=0.15, clicks=1, interval=0.0):
    """Clique seguro com verificação de cancelamento"""
    verificar_cancelamento()
    if clicks == 1:
        pyautogui.click(posicao, duration=duration)
    else:
        pyautogui.click(posicao, clicks=clicks, interval=interval, duration=duration)
    sleep_cancelamento(0.1)

def escrever(texto, intervalo=0.05):
    """Escreve texto simulando teclado"""
    verificar_cancelamento()
    pyautogui.write(texto, interval=intervalo)
    sleep_cancelamento(0.1)

# ------------------------------

clicar(aguardar_imagem('img/00.png'))
aguardar_imagem('img/01.png', timeout=2, continuar=True)
clicar(aguardar_imagem('img/02.png'))
pyautogui.hotkey('ctrl', 'v')
pyautogui.press('enter')
aguardar_imagem('img/03.png')
clicar((1059, 271))
clicar((817, 560))
clicar((1140, 510))
aguardar_imagem('img/04.png')
clicar((957, 429))
clicar((897, 482))
clicar((1084, 430))
escrever(nivelEnsino)
clicar((1140, 431))
clicar((1080, 654))
clicar((1096, 677))
