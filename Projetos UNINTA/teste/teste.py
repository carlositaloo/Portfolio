import pyautogui
import keyboard
import pyperclip
import time
import sys

senha = 'catucada1'

# Função para verificar se a tecla ESC foi pressionada
def verificar_cancelamento():
    if keyboard.is_pressed('esc'):
        print("Script cancelado pelo usuário.")
        sys.exit()  # Encerra o script imediatamente

def aguardar_imagem(imagem_path, timeout=30, intervalo=0.25, confidence=0.8):
    """Aguarda uma imagem aparecer na tela"""
    tempo_inicial = time.time()
    while time.time() - tempo_inicial < timeout:
        verificar_cancelamento()  # Verificar cancelamento durante a espera
        try:
            # MUDANÇA PRINCIPAL: Adicionado confidence
            posicao = pyautogui.locateOnScreen(imagem_path, confidence=confidence)
            if posicao:
                return posicao
        except pyautogui.ImageNotFoundException:
            pass
        except Exception as e:
            print(f"Erro ao procurar imagem: {e}")
        time.sleep(intervalo)
    raise TimeoutError(f"Imagem {imagem_path} não encontrada em {timeout}s")

# Configurações iniciais
timeset = 0.2  # Tempo de espera entre ações

# pyautogui.hotkey("win", "d")
verificar_cancelamento()
aguardar_imagem('img\\img0.png')
pyautogui.doubleClick(1861, 37, duration=0.15)
aguardar_imagem('img\\img1.png')
pyautogui.click(1092, 515, duration=0.15)
aguardar_imagem('img\\img2.png')
pyperclip.copy(senha)
pyautogui.click(947, 474, duration=0.15)
pyautogui.hotkey('ctrl', 'v')
pyautogui.press('enter')

aguardar_imagem('img\\img3.png')
pyautogui.click(105, 173, duration=0.15)
pyautogui.click(18, 45, duration=0.15)
aguardar_imagem('img\\img4.png')
pyautogui.click(99, 280, duration=0.15)
aguardar_imagem('img\\img5.png')
pyautogui.click(176, 41, duration=0.15)
pyautogui.click(176, 100, duration=0.15)