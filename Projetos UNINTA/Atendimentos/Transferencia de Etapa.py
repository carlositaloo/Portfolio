import pyautogui
import time
import keyboard
import pyperclip
import sys
import os

# Configurações iniciais
timeset = 0.1
# idatendimento = pyperclip.paste()
idatendimento = "1392216"
ticket = "883103"
etapa = ""

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


aguardar_imagem('img\\img0.png')
img1 = aguardar_imagem('img\\img1.png')

verificar_cancelamento()

pyautogui.click(img1, duration=0.15)
img2 = aguardar_imagem('img\\img2.png')
pyautogui.click(img2, duration=0.15)
pyautogui.write(idatendimento, interval=0.05)
img3 = aguardar_imagem('img\\img3.png')
pyautogui.click(img3, duration=0.15)

img4 = aguardar_imagem('img\\img4.png')
img5 = aguardar_imagem('img\\img5.png')
if img5:  # Se achou a imagem
    x, y = pyautogui.center(img5)  # pega o centro
    pyautogui.click(x, y + 100, duration=0.15)  # clica 100px abaixo
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.2)  # espera o SO processar o comando
    paste = pyperclip.paste()
pyautogui.doubleClick(x, y + 100, duration=0.15)

img6 = aguardar_imagem('img\\img6.png')
img7 = aguardar_imagem('img\\img7.png', numero=2)
if img7:  # Se achou a imagem
    x, y = pyautogui.center(img7)  # pega o centro
    pyautogui.click(x, y + 10, duration=0.15)  # clica 100px abaixo
img8 = aguardar_imagem('img\\img8.png')
pyautogui.hotkey('ctrl', 'a')
img9 = aguardar_imagem('img\\img9.png')
pyautogui.click(img9, duration=0.15)
img10 = aguardar_imagem('img\\img10.png')
if img10:
    x = img10.left
    y = img10.top
    pyautogui.click(x + 10, y + 10, duration=0.15)

img11 = aguardar_imagem('img\\img11.png')
pyautogui.press('tab')
pyperclip.copy(paste)
pyautogui.hotkey('ctrl', 'v')
pyautogui.press('tab')
pyautogui.press('tab')
pyautogui.press('tab')

pyautogui.write(f'Solicitação via ticket: {ticket}', interval=0.05)
# pyautogui.write('Correcao de atendimento')

pyautogui.press('tab')
pyautogui.press('tab')
pyperclip.copy(etapa)
pyautogui.hotkey('ctrl', 'v')
pyautogui.press('tab')
pyautogui.press('tab')
pyautogui.press('tab')    
pyautogui.write('47')
pyautogui.press('tab')
pyautogui.press('tab')



# aguardar_imagem('img\\filtro.png')
# pyautogui.write(usuario, interval=0.05)
# pyautogui.press('enter')
# pyautogui.click(213, 358, duration=0.15)
# time.sleep(0.5)  # Espera a tela carregar
# pyautogui.hotkey('ctrl', 'c')

# verificar_cancelamento()

# pyautogui.click(pessoas, duration=0.15)
# pyautogui.click(130, 227, duration=0.15)
# aguardar_imagem('img\\filtro.png')
# pyautogui.hotkey('ctrl', 'v')
# pyautogui.press('enter')
# time.sleep(0.5)  # Espera a tela carregar

# verificar_cancelamento()

# pyautogui.doubleClick(673, 337, duration=0.15)
# aguardar_imagem('img\\pessoa.png')
# pyautogui.click(630, 372, duration=0.15)
# time.sleep(0.5)
# pyautogui.click(859, 319, duration=0.15)
# pyautogui.hotkey('ctrl', 'a')
# pyautogui.hotkey('ctrl', 'c')
# time.sleep(0.2)  # espera o SO processar o comando
# conteudo = pyperclip.paste()
# numeros = ''.join(ch for ch in conteudo if ch.isdigit())
# pyperclip.copy(numeros)

# verificar_cancelamento()

# pyautogui.click(iusuario, duration=0.15)
# pyautogui.doubleClick(213, 358, duration=0.15)
# time.sleep(0.5)
# pyautogui.click(743, 597, duration=0.15)
# time.sleep(0.5)
# pyautogui.click(964, 479, duration=0.15)
# pyautogui.hotkey('ctrl', 'v')
# pyautogui.click(967, 517, duration=0.15)
# pyautogui.hotkey('ctrl', 'v')
# pyautogui.click(945, 609, duration=0.15)
# pyautogui.click(1099, 718, duration=0.15)
