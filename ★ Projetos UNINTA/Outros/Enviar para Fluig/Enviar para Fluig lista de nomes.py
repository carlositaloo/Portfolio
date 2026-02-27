import pyautogui
import pyperclip
import time
import keyboard
import os


# Configurações iniciais
timeset = 0.1
script_dir = os.path.dirname(os.path.abspath(__file__))

nomes = [
    "MARCELO JUNIOR DA SILVEIRA",
    "TEMOTIO SILVA FERREIRA GOMES",
    "ROBERIO MOREIRA GOMES DA SILVA",
    "GERALDO EDICARLOS DE SOUSA",
    "FRANCISCO EVANDRO BARBOS DE SOUSA",
]


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

def clicar(posicao, duration=0.15, clicks=1, interval=0.0):
    """Clique seguro com verificação de cancelamento"""
    verificar_cancelamento()
    if clicks == 1:
        pyautogui.click(posicao, duration=duration)
    else:
        pyautogui.click(posicao, clicks=clicks, interval=interval, duration=duration)
    sleep_cancelamento(0.1)

def atalho(teclas, duration=0.1):
    """
    Pressiona um atalho de teclado ou tecla única com verificação de cancelamento
    
    Args:
        teclas: String para tecla única ('enter') ou tupla/lista para combinação (('ctrl', 'a'))
        duration: Intervalo entre as teclas
    """
    verificar_cancelamento()
    
    # Verifica se é uma string (tecla única) ou tupla/lista (combinação)
    if isinstance(teclas, str):
        pyautogui.press(teclas)
    else:
        pyautogui.hotkey(*teclas, interval=duration)
    
    sleep_cancelamento(0.1)

# clicar(aguardar_imagem('img\\menu.png', click='bottomleft'))  # MENU
# clicar(aguardar_imagem('img\\servicosGlobais.png'))  # SERVIÇOS GLOBAIS
# clicar(aguardar_imagem('img\\avisoGlobais.png', click='bottomright'))  # AVISO SERVIÇOS GLOBAIS
# clicar(aguardar_imagem('img\\seguranca.png'))  # SEGURANÇA
# clicar(aguardar_imagem('img\\usuarios.png'))  # USUÁRIOS

for nome in nomes:
    clicar(aguardar_imagem('img\\porNome.png'))  # POR NOME
    pyperclip.copy(nome)
    time.sleep(1)  # Pequena pausa para garantir que o texto foi copiado
    atalho(('ctrl', 'v'))  # COLAR NOME
    atalho('enter')  # PESQUISAR
    
    usuario_encontrado = aguardar_imagem('img\\selecionarUsuario.png', click='bottomright', timeout=3, confidence=0.9, continuar=True)
    
    if usuario_encontrado:
        clicar(usuario_encontrado)
        #Aguardar apertar f9
        while True:
            verificar_cancelamento()
            if keyboard.is_pressed('f9'):
                print("F9 pressionado, continuando com o próximo ciclo.")
                time.sleep(0.1)  # evita múltiplas detecções
                break
            time.sleep(0.1)  # Pequena pausa para evitar uso excessivo da CPU
        
        clicar(aguardar_imagem('img\\processos.png', click='bottomright'))  # PROCESSOS
        clicar(aguardar_imagem('img\\enviarGED.png'))  # ENVIAR
        clicar(aguardar_imagem('img\\aguardarGED.png', timeout=60))  # AGUARDAR CARREGAMENTO DO GED
        clicar(aguardar_imagem('img\\avancaGED.png'))  # CONFIRMAR ENVIO
        clicar(aguardar_imagem('img\\executarGED.png'))  # EXECUTAR
        clicar(aguardar_imagem('img\\sucessoGED.png', timeout=180))  # AGUARDAR SUCESSO
        clicar(aguardar_imagem('img\\fecharGED.png'))  # FECHAR MENSAGEM DE SUCESSO
        clicar(aguardar_imagem('img\\okGED.png', click='bottomright'))  # OK PARA VOLTAR PARA A TELA DE USUÁRIOS
        print(f"Processo de envio para {nome} concluído com sucesso.")
        time.sleep(1)  # Pequena pausa antes de iniciar o próximo ciclo
    else:
        print(f"Usuário {nome} não encontrado, pulando para o próximo.")
        time.sleep(1)  # Pequena pausa antes de iniciar o próximo ciclo
