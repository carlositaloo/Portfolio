import pyautogui
import time
import keyboard
import sys
import os

# Configurações iniciais
timeset = 0.1

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


pyautogui.click(17, 43, duration=0.15) # MENU
aguardar_imagem('img\\menu0.png')
pyautogui.click(107, 283, duration=0.15) # SERVIÇO GLOBAIS
sleep_cancelamento(timeset)
img = aguardar_imagem('img\\erro.png')
pyautogui.click(img, duration=0.15)
sleep_cancelamento(timeset)
aguardar_imagem('img\\cortina0.png')
pyautogui.click(179, 44, duration=0.15) # SUB MENU
aguardar_imagem('img\\usuario.png')
pyautogui.click(176, 94, duration=0.15) # USUARIOS
aguardar_imagem('img\\img0.png')
pyautogui.click(17, 43, duration=0.15) # MENU
aguardar_imagem('img\\menu0.png')
pyautogui.click(129, 110, duration=0.15) # EDUCACIONAL
pyautogui.click(341, 125, duration=0.15) # EDUCACIONAL
aguardar_imagem('img\\educacional.png')
pyautogui.click(27, 82, duration=0.15) # ALUNO
aguardar_imagem('img\\img1.png')
pyautogui.click(79, 84, duration=0.15) # PROFESSOR
aguardar_imagem('img\\img2.png')
pyautogui.click(17, 43, duration=0.15) # MENU
aguardar_imagem('img\\menu0.png')
pyautogui.click(165, 86, duration=0.15) # RH
pyautogui.click(386, 157, duration=0.15) # GESTÃO DE PESSOAS
aguardar_imagem('img\\cortina1.png')
pyautogui.click(207, 42, duration=0.15) # SUB MENU
aguardar_imagem('img\\acompanhamento.png')
pyautogui.click(42, 72, duration=0.15) # FUNCIONARIO
aguardar_imagem('img\\img3.png')
pyautogui.click(94, 85, duration=0.15) # PESSOAS
aguardar_imagem('img\\img4.png')
pyautogui.click(17, 43, duration=0.15) # MENU
aguardar_imagem('img\\menu0.png')
pyautogui.click(129, 110, duration=0.15) # EDUCACIONAL
pyautogui.click(341, 125, duration=0.15) # EDUCACIONAL
aguardar_imagem('img\\disciplina.png')
pyautogui.click(768, 93, duration=0.15) # DISCIPLINA

