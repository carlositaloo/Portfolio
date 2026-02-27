import pyautogui
import time
import keyboard
import sys
import os
import pyperclip
from datetime import datetime, timedelta

# ------------------------------
# Configurações iniciais
# ------------------------------
timeset = 0.1

# Determina o diretório base (funciona tanto para script quanto para exe)
if getattr(sys, 'frozen', False):
    # Se executado como exe (PyInstaller)
    # Diretório do executável para logs
    exe_dir = os.path.dirname(sys.executable)
    # Diretório temporário onde o PyInstaller extrai os recursos
    script_dir = sys._MEIPASS
else:
    # Se executado como script Python
    exe_dir = os.path.dirname(os.path.abspath(__file__))
    script_dir = os.path.dirname(os.path.abspath(__file__))

log_dir = os.path.join(exe_dir, 'logs')  # Logs ao lado do .exe

# Criar pasta de logs se não existir
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
    print(f"Pasta de logs criada: {log_dir}")

# ------------------------------
# Funções utilitárias
# ------------------------------

def capturar_tela():
    """Captura a tela e salva com timestamp"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"screenshot_{timestamp}.png"
        caminho_completo = os.path.join(log_dir, nome_arquivo)
        
        screenshot = pyautogui.screenshot()
        screenshot.save(caminho_completo)
        
        print(f"Screenshot salvo: {nome_arquivo}")
        return caminho_completo
    except Exception as e:
        print(f"Erro ao capturar tela: {e}")
        return None

def verificar_cancelamento():
    """Cancela a execução atual se ESC for pressionado"""
    try:
        if keyboard.is_pressed('esc'):
            print("Execução cancelada pelo usuário (ESC).")
            time.sleep(0.9)
            raise KeyboardInterrupt("ESC pressionado")
    except KeyboardInterrupt:
        raise
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

def aguardar_imagem(imagem_path, timeout=30, intervalo=0.1, confidence=0.99, continuar=False, click='center'):
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

# ------------------------------
# Função principal de execução
# ------------------------------

def executar_automacao():
    """Executa a automação uma vez"""
    try:
        print("\n" + "="*50)
        print("Iniciando execução...")
        print("="*50)
        
        # CAPTURA A TELA ANTES DE EXECUTAR
        print("\nCapturando tela para log...")
        capturar_tela()
        
        aguardar_imagem('img\\01.png')
        verificar_cancelamento()
        img2 = aguardar_imagem('img\\02.png')
        verificar_cancelamento()
        img3 = aguardar_imagem('img\\03.png')
        verificar_cancelamento()

        clicar(img2+(0, 30))
        verificar_cancelamento()
        clicar(img2+(0, 130))
        verificar_cancelamento()
        
        clicar(img3+(0, 30))
        verificar_cancelamento()
        
        keyboard.send('ctrl+a')
        verificar_cancelamento()
        keyboard.send('ctrl+c')
        time.sleep(0.2)
        verificar_cancelamento()
        data_str = pyperclip.paste()
        verificar_cancelamento()
        print(f"Conteúdo copiado: {data_str}")
        verificar_cancelamento()

        data = datetime.strptime(data_str, "%d/%m/%Y")
        verificar_cancelamento()
        nova_data = data + timedelta(days=1)
        verificar_cancelamento()
        pyperclip.copy(nova_data.strftime("%d/%m/%Y"))
        verificar_cancelamento()

        keyboard.send('ctrl+v')
        verificar_cancelamento()

        img4 = aguardar_imagem('img\\04.png')
        verificar_cancelamento()
        clicar(img4)
        time.sleep(0.6)
        verificar_cancelamento()

        clicar(img2+(0, 30))
        verificar_cancelamento()
        clicar(img2+(0, 150))
        verificar_cancelamento()
        
        clicar(img3+(0, 30))
        verificar_cancelamento()
        keyboard.send('ctrl+a')
        verificar_cancelamento()
        pyperclip.copy(data_str)
        time.sleep(0.2)
        verificar_cancelamento()
        keyboard.send('ctrl+v')
        verificar_cancelamento()
        clicar(img4)
        time.sleep(0.6)
        verificar_cancelamento()
        
        print("="*50)
        print("Execução concluída com sucesso!")
        print("="*50)
        
        img5 = aguardar_imagem('img\\05.png')
        clicar(img5+(0, -30))
        verificar_cancelamento()
        
    except KeyboardInterrupt:
        print("\nExecução interrompida (ESC). Aguardando F9 para nova execução...")
    except Exception as e:
        print(f"\nErro durante execução: {e}")
        print("Aguardando F9 para nova execução...")

# ------------------------------
# Loop principal
# ------------------------------

if __name__ == "__main__":
    print("="*50)
    print("AUTOMAÇÃO INICIADA")
    print("="*50)
    print("Comandos:")
    print("  F9  - Executar automação")
    print("  ESC - Cancelar execução atual")
    print("="*50)
    print(f"Logs salvos em: {log_dir}")
    print("="*50)
    print("\nAguardando comando...")
    
    executando = True
    
    while executando:
        try:
            # Verifica F9 para executar
            if keyboard.is_pressed('f9'):
                time.sleep(0.3)  # Evita múltiplas detecções
                while True:
                    executar_automacao()
                    time.sleep(0.5)  # Pequeno delay entre execuções
                    img6 = aguardar_imagem('img\\06.png', timeout=1, continuar=True, confidence=0.99)
                    if img6:
                        executar_automacao()
                        print("\nImagem 06 encontrada. Voltando ao modo de espera...")
                        break
            
            time.sleep(0.1)  # Pequeno delay para não sobrecarregar CPU
            
        except KeyboardInterrupt:
            print("\n" + "="*50)
            print("Programa interrompido")
            print("="*50)
            executando = False
        except Exception as e:
            print(f"\nErro no loop principal: {e}")
            time.sleep(1)
    
    sys.exit(0)