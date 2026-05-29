import pyautogui
import time
import keyboard
import sys
import os
import pyperclip
from datetime import datetime, timedelta

# ------------------------------
# Diretório base
# ------------------------------
if getattr(sys, 'frozen', False):
    exe_dir = os.path.dirname(sys.executable)
    script_dir = sys._MEIPASS
else:
    exe_dir = os.path.dirname(os.path.abspath(__file__))
    script_dir = os.path.dirname(os.path.abspath(__file__))

log_dir = os.path.join(exe_dir, 'logs')

if not os.path.exists(log_dir):
    os.makedirs(log_dir)
    print(f"Pasta de logs criada: {log_dir}")

# ------------------------------
# Seleção de modo
# ------------------------------

def selecionar_modo():
    print("=" * 50)
    print("  RESYNC DISCIPLINAS EAD → AVA (TOTVS)")
    print("=" * 50)
    print("  [1] Manual (com pausa)")
    print("      Processa UMA disciplina EAD por F9")
    print("      Ideal para reenviar uma disciplina específica")
    print()
    print("  [2] Automático (em lote)")
    print("      Percorre todas as disciplinas EAD do aluno")
    print("      Pula automaticamente as disciplinas presenciais")
    print("=" * 50)
    while True:
        escolha = input("  Digite 1 ou 2: ").strip()
        if escolha in ('1', '2'):
            return int(escolha)
        print("  Opção inválida. Digite 1 ou 2.")

MODO = selecionar_modo()

# Configurações dependentes do modo
CONFIDENCE   = 0.9  if MODO == 1 else 0.99
CANCEL_SLEEP = 0.3  if MODO == 1 else 0.9
NOME_MODO    = "Manual (com pausa)" if MODO == 1 else "Automático (em lote)"

# ------------------------------
# Funções utilitárias
# ------------------------------

def capturar_tela():
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
    try:
        if keyboard.is_pressed('esc'):
            print("Execução cancelada pelo usuário (ESC).")
            time.sleep(CANCEL_SLEEP)
            raise KeyboardInterrupt("ESC pressionado")
    except KeyboardInterrupt:
        raise
    except Exception:
        pass

def sleep_cancelamento(duration):
    elapsed = 0
    while elapsed < duration:
        verificar_cancelamento()
        sleep_time = min(0.1, duration - elapsed)
        time.sleep(sleep_time)
        elapsed += sleep_time

def aguardar_imagem(imagem_path, timeout=30, intervalo=0.1, confidence=None, continuar=False, click='center'):
    if confidence is None:
        confidence = CONFIDENCE
    caminho_completo = os.path.join(script_dir, imagem_path)
    inicio = time.time()
    while time.time() - inicio < timeout:
        verificar_cancelamento()
        try:
            posicao = pyautogui.locateOnScreen(caminho_completo, confidence=confidence)
            if posicao:
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
                    ponto = (x + largura // 2, y + altura // 2)
                return ponto
        except Exception:
            pass
        sleep_cancelamento(intervalo)
    if continuar:
        return None
    else:
        raise TimeoutError(f"Imagem {imagem_path} não encontrada em {timeout}s")

def clicar(posicao, duration=0.15, clicks=1, interval=0.0):
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
    """
    Verifica se a disciplina é EAD e executa o fix de resync no TOTVS → AVA.
    - Se EAD     : faz o fix (muda data +1 dia e volta) e avança para a próxima
    - Se presencial: pula sem tocar (modo automático avança, modo manual só avisa)
    """
    try:
        print("\n" + "=" * 50)
        print("Verificando tipo da disciplina...")
        print("=" * 50)

        # ── Verifica se é EAD antes de qualquer ação ──
        img7 = aguardar_imagem('img\\07.png', timeout=60, continuar=True)
        if not img7:
            print("  Disciplina NÃO é EAD (presencial). Pulando...")
            if MODO == 2:
                img5 = aguardar_imagem('img\\05.png', continuar=True)
                if img5:
                    clicar(img5 + (0, -30))
                    sleep_cancelamento(0.5)
            return  # sem True/False — simplesmente sai

        print("  Disciplina EAD confirmada. Iniciando resync...")
        print("=" * 50)

        print("\nCapturando tela para log...")
        capturar_tela()

        sleep_cancelamento(0.5)

        aguardar_imagem('img\\01.png')
        verificar_cancelamento()
        img2 = aguardar_imagem('img\\02.png')
        verificar_cancelamento()
        img3 = aguardar_imagem('img\\03.png')
        verificar_cancelamento()

        clicar(img2 + (0, 30))
        verificar_cancelamento()
        clicar(img2 + (0, 130))
        verificar_cancelamento()

        clicar(img3 + (0, 30))
        verificar_cancelamento()

        keyboard.send('ctrl+a')
        verificar_cancelamento()

        sleep_cancelamento(0.2)

        keyboard.send('ctrl+c')
        verificar_cancelamento()
        sleep_cancelamento(0.2)
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
        sleep_cancelamento(0.6)
        verificar_cancelamento()

        clicar(img2 + (0, 30))
        verificar_cancelamento()
        clicar(img2 + (0, 150))
        verificar_cancelamento()

        clicar(img3 + (0, 30))
        verificar_cancelamento()

        keyboard.send('ctrl+a')

        sleep_cancelamento(0.2)

        verificar_cancelamento()
        pyperclip.copy(data_str)
        sleep_cancelamento(0.2)
        verificar_cancelamento()
        keyboard.send('ctrl+v')
        verificar_cancelamento()
        clicar(img4)
        verificar_cancelamento()

        print("=" * 50)
        print("Execução concluída com sucesso!")
        print("=" * 50)

        img5 = aguardar_imagem('img\\05.png')
        verificar_cancelamento()

        if MODO == 1:
            pyautogui.moveTo(img5 + (0, -30), duration=0.3)  # só move o mouse
        else:
            clicar(img5 + (0, -30))  # clica para avançar ao próximo registro

        verificar_cancelamento()

    except KeyboardInterrupt:
        print("\nExecução interrompida (ESC).")
        raise  # sobe o ESC para o loop do lote poder parar
    except Exception as e:
        print(f"\nErro durante execução: {e}")
        print("Aguardando F9 para nova execução...")

# ------------------------------
# Loop principal
# ------------------------------

if __name__ == "__main__":
    print("=" * 50)
    print("  RESYNC DISCIPLINAS EAD → AVA (TOTVS)")
    print(f"  Modo: {NOME_MODO}")
    print("=" * 50)
    print("  Comandos:")
    print("    F9  - Executar (verifica EAD antes de agir)")
    print("    ESC - Cancelar execução atual")
    print("=" * 50)
    print(f"  Logs salvos em: {log_dir}")
    print("=" * 50)
    print("\n  Aguardando comando...")

    executando = True

    while executando:
        try:
            if keyboard.is_pressed('f9'):
                time.sleep(0.3)  # Evita múltiplas detecções

                if MODO == 1:
                    # ── Modo manual: uma execução por F9 ──
                    try:
                        executar_automacao()
                    except KeyboardInterrupt:
                        print("  Execução cancelada (ESC).")
                    print("\n  Aguardando novo comando (F9 para executar)...")
                else:
                    # ── Modo automático: repete até encontrar img06 (fim da lista) ──
                    # A cada iteração, executar_automacao() verifica EAD:
                    #   - EAD      → faz o fix e clica img5 (próxima)
                    #   - Presencial → apenas clica img5 (próxima)
                    # Em ambos os casos, depois verifica img6 (fim da lista)
                    try:
                        while True:
                            executar_automacao()
                            sleep_cancelamento(0.3)
                            img6 = aguardar_imagem('img\\06.png', timeout=0.5, continuar=True, confidence=0.99)
                            if img6:
                                executar_automacao()  # processa a última antes de parar
                                print("\n  Fim da lista. Voltando ao modo de espera...")
                                break
                    except KeyboardInterrupt:
                        print("\n  Lote cancelado (ESC). Voltando ao modo de espera...")

            time.sleep(0.1)

        except KeyboardInterrupt:
            print("\n" + "=" * 50)
            print("  Programa interrompido")
            print("=" * 50)
            executando = False
        except Exception as e:
            print(f"\nErro no loop principal: {e}")
            time.sleep(1)

    sys.exit(0)
