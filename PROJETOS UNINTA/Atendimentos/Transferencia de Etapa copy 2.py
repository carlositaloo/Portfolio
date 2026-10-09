import pyautogui
import time
import keyboard
import pyperclip
import sys
import os

# Configurações iniciais
timeset = 0.1
# idatendimento = pyperclip.paste()
idatendimento = "1494087"
ticket = "153302"
etapa = "Análise da Tesouraria"
mensagem = f"Solicitação via ticket: {ticket}"
print(mensagem)

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


def aguardar_imagem(imagem_path, timeout=30, intervalo=0.1, confidence=0.9, continuar=False, click='center'):
    """
    Aguarda uma imagem aparecer na tela
    
    Args:
        click: Define o ponto de clique na imagem encontrada
               - 'center': centro da imagem (padrão)
               - 'topleft': canto superior esquerdo
               - 'topright': canto superior direito
               - 'bottomleft': canto inferior esquerdo
               - 'bottomright': canto inferior direito
    """
    caminho_completo = os.path.join(script_dir, imagem_path)
    inicio = time.time()
    while time.time() - inicio < timeout:
        verificar_cancelamento()
        try:
            posicao = pyautogui.locateOnScreen(caminho_completo, confidence=confidence)
            if posicao:
                # Calcular a posição do clique baseado no parâmetro click
                x, y, largura, altura = posicao
                
                if click == 'center':
                    ponto = (x + largura // 2, y + altura // 2)
                elif click == 'topleft':
                    ponto = (x, y)
                elif click == 'topright':
                    ponto = (x + largura, y)
                elif click == 'bottomleft':
                    ponto = (x, y + altura)
                elif click == 'bottomright':
                    ponto = (x + largura, y + altura)
                else:
                    # Padrão: centro
                    ponto = (x + largura // 2, y + altura // 2)
                
                return ponto
        except Exception as e:
            # Ignora exceções comuns de imagem não encontrada
            pass
        sleep_cancelamento(intervalo)
    if continuar:
        return None
    else:
        raise TimeoutError(f"Imagem {imagem_path} não encontrada em {timeout}s")


verificar_cancelamento()

img1 = aguardar_imagem('img\\seletor.png', click='bottomright')
pyautogui.click(img1, duration=0.15)
x, y = aguardar_imagem('img\\processo.png')
pyautogui.click(x + 38, y, duration=0.15)
img3 = aguardar_imagem('img\\em andamento.png')
pyautogui.click(img3, duration=0.15)
img4 = aguardar_imagem('img\\error.png', continuar=True, timeout=5)
if img4:
    keyboard.press('enter')
aguardar_imagem('img\\confirmar andamento.png')
img5 = aguardar_imagem('img\\executar.png')
pyautogui.click(img5, duration=0.15)
img5 = aguardar_imagem('img\\fechar.png')
pyautogui.click(img5, duration=0.15)