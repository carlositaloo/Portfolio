import pyautogui
import time
import keyboard
import sys
import os

# ------------------------------
# Configurações iniciais
# ------------------------------
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
            # Ignora exceções comuns de imagem não encontrada
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

# ------------------------------
# Execução do script
# ------------------------------

# Abrir menu principal e acessar Serviços Globais
clicar((17, 43))  # MENU
aguardar_imagem('img\\menu0.png')
clicar((107, 283))  # SERVIÇOS GLOBAIS
sleep_cancelamento(timeset)

# Tratar possível erro
img_erro = aguardar_imagem('img\\erro.png')
clicar(img_erro)
sleep_cancelamento(timeset)

# Acessar Usuários
aguardar_imagem('img\\cortina0.png')
clicar((179, 44))  # SUB MENU
aguardar_imagem('img\\usuario.png')
clicar((176, 94))  # USUÁRIOS
aguardar_imagem('img\\img0.png')

# Navegar para Educacional - Aluno
clicar((17, 43))  # MENU
aguardar_imagem('img\\menu0.png')
clicar((129, 110))  # EDUCACIONAL
clicar((341, 125))  # EDUCACIONAL
aguardar_imagem('img\\educacional.png')
clicar((27, 82))  # ALUNO
aguardar_imagem('img\\img1.png')

# Interações na tela de Aluno
aguardar_imagem('img\\anexos.png')
clicar((440, 197))
sleep_cancelamento(timeset)
clicar((480, 265))
sleep_cancelamento(timeset)
clicar((837, 441))
sleep_cancelamento(timeset)
clicar((1158, 552))
sleep_cancelamento(timeset)

# Acessar Professor
clicar((79, 78))  # PROFESSOR
while True:
    resultado = aguardar_imagem('img\\img2.png', timeout=3.5, continuar=True)
    if resultado:
        break
    else:
        clicar((79, 78))  # PROFESSOR

# Navegar para RH - Gestão de Pessoas - Funcionário
clicar((17, 43))  # MENU
aguardar_imagem('img\\menu0.png')
clicar((165, 86))  # RH
clicar((386, 157))  # GESTÃO DE PESSOAS
aguardar_imagem('img\\cortina1.png')
clicar((207, 42))  # SUB MENU
aguardar_imagem('img\\acompanhamento.png')
clicar((42, 72))  # FUNCIONÁRIO
aguardar_imagem('img\\img3.png')

# Acessar Disciplina (comentado: acesso a Pessoas)
clicar((94, 85))  # PESSOAS
aguardar_imagem('img\\img4.png')
clicar((17, 43))  # MENU
aguardar_imagem('img\\menu0.png')
clicar((129, 110))  # EDUCACIONAL
clicar((341, 125))  # EDUCACIONAL
aguardar_imagem('img\\disciplina.png')
clicar((768, 93))  # DISCIPLINA

print("Script concluído com sucesso!")