import pyautogui
import time
import keyboard
import pyperclip
import sys
import os

# ------------------------------
# Configurações iniciais
# ------------------------------
timeset = 0.1
usuario = pyperclip.paste().strip()
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

def aguardar_imagem(imagem_path, timeout=30, intervalo=0.1, confidence=0.8):
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

def copiar_texto():
    """Copia do clipboard após selecionar"""
    verificar_cancelamento()
    pyautogui.hotkey('ctrl', 'c')
    sleep_cancelamento(0.2)
    return pyperclip.paste()

def colar_texto():
    """Cola do clipboard"""
    verificar_cancelamento()
    pyautogui.hotkey('ctrl', 'v')
    sleep_cancelamento(0.1)

# ------------------------------
# Execução do script
# ------------------------------

# Localizar imagens principais
iusuario = aguardar_imagem('img\\usuario.png')
pessoas = aguardar_imagem('img\\pessoas.png')
porusuario = aguardar_imagem('img\\porusuario.png')

# Preencher filtro por usuário
clicar(porusuario)
aguardar_imagem('img\\filtro.png')
escrever(usuario)
pyautogui.press('enter')
aguardar_imagem('img\\select.png')
clicar((213, 358))
sleep_cancelamento(0.5)
copiar_texto()  # Ctrl+C

# Preencher filtro na aba "pessoas"
clicar(pessoas)
sleep_cancelamento(0.1)
clicar((130, 227))
aguardar_imagem('img\\filtro.png')
colar_texto()
pyautogui.press('enter')
aguardar_imagem('img\\select.png')

# Selecionar pessoa e copiar números
clicar((673, 337), clicks=2)
aguardar_imagem('img\\pessoa.png')
clicar((630, 372))
sleep_cancelamento(0.5)
clicar((859, 319))
pyautogui.hotkey('ctrl', 'a')
numeros = ''.join(ch for ch in copiar_texto() if ch.isdigit())
pyperclip.copy(numeros)

# Atualizar dados do usuário
clicar(iusuario)
aguardar_imagem('img\\select.png')
clicar((213, 358), clicks=2)
aguardar_imagem('img\\usuario_detalhe.png')
clicar((743, 597))
aguardar_imagem('img\\alterar_senha.png')
clicar((964, 479))
colar_texto()
clicar((967, 517))
colar_texto()
sleep_cancelamento(0.1)
clicar((945, 609))
if aguardar_imagem('img\\senha_login.png', timeout=4):
    clicar((643, 655))
sleep_cancelamento(0.1)
clicar((1099, 718))
sleep_cancelamento(0.1)

# Mensagem final no clipboard
pyperclip.copy(f"""
A senha do usuário {usuario} foi redefinida para o CPF do mesmo (somente números). Ao acessar pela primeira vez, será solicitado que altere a senha:

• No primeiro campo, insira a senha atual (CPF do usuário).
• Nos campos seguintes, digite a nova senha e confirme.
""")
