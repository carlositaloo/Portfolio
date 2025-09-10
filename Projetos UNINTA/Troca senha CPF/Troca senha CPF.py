import pyautogui
import time
import keyboard
import pyperclip
import sys
import os

# Configurações iniciais
timeset = 0.1
usuario = pyperclip.paste()

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


def aguardar_imagem(imagem_path, timeout=30, intervalo=0.1, confidence=0.8):
    """Aguarda uma imagem aparecer na tela"""
    # Correção: construir caminho absoluto
    caminho_completo = os.path.join(script_dir, imagem_path)
    
    tempo_inicial = time.time()
    while time.time() - tempo_inicial < timeout:
        verificar_cancelamento()
        try:
            posicao = pyautogui.locateOnScreen(caminho_completo, confidence=confidence)
            if posicao:
                return posicao
        except pyautogui.ImageNotFoundException:
            pass
        except Exception as e:
            print(f"Erro ao procurar imagem: {e}")

        # Usa sleep com verificação de cancelamento
        sleep_cancelamento(intervalo)
    raise TimeoutError(f"Imagem {imagem_path} não encontrada em {timeout}s")


aguardar_imagem('img\\usuario.png')
aguardar_imagem('img\\pessoas.png')
iusuario = aguardar_imagem('img\\usuario.png')
pessoas = aguardar_imagem('img\\pessoas.png')
porusuario = aguardar_imagem('img\\porusuario.png')

verificar_cancelamento()

pyautogui.click(iusuario, duration=0.15)
pyautogui.click(porusuario, duration=0.15)
aguardar_imagem('img\\filtro.png')
pyautogui.write(usuario, interval=0.05)
pyautogui.press('enter')
pyautogui.click(213, 358, duration=0.15)
time.sleep(0.5)  # Espera a tela carregar
pyautogui.hotkey('ctrl', 'c')

verificar_cancelamento()

pyautogui.click(pessoas, duration=0.15)
pyautogui.click(130, 227, duration=0.15)
aguardar_imagem('img\\filtro.png')
pyautogui.hotkey('ctrl', 'v')
pyautogui.press('enter')
time.sleep(0.5)  # Espera a tela carregar

verificar_cancelamento()

pyautogui.doubleClick(673, 337, duration=0.15)
aguardar_imagem('img\\pessoa.png')
pyautogui.click(630, 372, duration=0.15)
time.sleep(0.5)
pyautogui.click(859, 319, duration=0.15)
pyautogui.hotkey('ctrl', 'a')
pyautogui.hotkey('ctrl', 'c')
time.sleep(0.2)  # espera o SO processar o comando
conteudo = pyperclip.paste()
numeros = ''.join(ch for ch in conteudo if ch.isdigit())
pyperclip.copy(numeros)

verificar_cancelamento()

pyautogui.click(iusuario, duration=0.15)
pyautogui.doubleClick(213, 358, duration=0.15)
time.sleep(0.5)
pyautogui.click(743, 597, duration=0.15)
time.sleep(0.5)
pyautogui.click(964, 479, duration=0.15)
pyautogui.hotkey('ctrl', 'v')
pyautogui.click(967, 517, duration=0.15)
pyautogui.hotkey('ctrl', 'v')
pyautogui.click(945, 609, duration=0.15)
pyautogui.click(1099, 718, duration=0.15)

pyperclip.copy(f'''
A senha do usuário {usuario} foi redefinida para o CPF do mesmo (somente números). Ao acessar pela primeira vez, será solicitado que altere a senha:

• No primeiro campo, insira a senha atual (CPF do usuário).
• Nos campos seguintes, digite a nova senha e confirme.
''')


