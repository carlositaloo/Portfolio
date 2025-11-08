import pyautogui
import time
import keyboard
import pyperclip
import sys
import os

# Configurações iniciais
timeset = 0.3
nivel = "1"


# Correção do caminho - adicione apenas estas 2 linhas
script_dir = os.path.dirname(os.path.abspath(__file__))


def verificar_cancelamento():
    try:
        if keyboard.is_pressed('esc'):
            print("Script cancelado pelo usuário.")
            time.sleep(0.1)  # Evita múltiplas detecções
            # Verifica novamente para confirmar
            if keyboard.is_pressed('esc'):
                sys.exit()
    except Exception:
        # Continua executando se houver erro na detecção
        pass


def sleep_cancelamento(duration):
    """Sleep que verifica ESC a cada 0.1s"""
    elapsed = 0
    while elapsed < duration:
        verificar_cancelamento()
        sleep_time = min(0.1, duration - elapsed)
        time.sleep(sleep_time)
        elapsed += sleep_time


def aguardar_imagem(imagem_path, numero=1, timeout=30, intervalo=0.1, confidence=0.8):
    """
    Aguarda uma imagem aparecer na tela.
    numero: qual ocorrência da imagem retornar (1 = primeira, 2 = segunda, etc.)
    """
    caminho_completo = os.path.join(script_dir, imagem_path)
    tempo_inicial = time.time()

    while time.time() - tempo_inicial < timeout:
        verificar_cancelamento()
        try:
            todas = list(pyautogui.locateAllOnScreen(
                caminho_completo, confidence=confidence))
            if len(todas) >= numero:
                return todas[numero - 1]  # retorna a n-ésima ocorrência
        except Exception as e:
            pass
        sleep_cancelamento(intervalo)

    raise TimeoutError(
        f"Imagem {imagem_path} (ocorrência {numero}) não encontrada em {timeout}s")


pyautogui.click(24, 166, duration=0.15)
time.sleep(timeset)
pyautogui.click(143, 249, duration=0.15)
pyautogui.hotkey('ctrl', 'v')
time.sleep(timeset)
pyautogui.click(1000, 624, duration=0.15)
time.sleep(timeset)
pyautogui.click(1062, 274, duration=0.15)
time.sleep(timeset)
pyautogui.click(811, 564, duration=0.15)
time.sleep(timeset)
pyautogui.click(1121, 508, duration=0.15)
time.sleep(timeset)
pyautogui.click(960, 427, duration=0.15)
time.sleep(timeset)
pyautogui.click(859, 484, duration=0.15)
time.sleep(timeset)
pyautogui.click(1095, 431, duration=0.15)
time.sleep(timeset)
pyautogui.write(nivel, interval=0.05)
time.sleep(timeset)
pyautogui.click(1141, 427, duration=0.15)
time.sleep(timeset)
pyautogui.click(1078, 662, duration=0.15)
time.sleep(timeset)
pyautogui.click(1099, 674, duration=0.15)