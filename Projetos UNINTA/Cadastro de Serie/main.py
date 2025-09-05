import pyautogui
import keyboard
import time
import sys
import os

# Configurações iniciais
timeset = 0.4

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

def aguardar_imagem(imagem_path, timeout=130, intervalo=0.25, confidence=0.8):
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

def digitar_teclas(texto, delay=0.1):
    for caractere in texto:
        keyboard.press_and_release(caractere)
        if delay > 0:
            time.sleep(delay)
    keyboard.press_and_release('right')
    keyboard.press_and_release('n')
    keyboard.press_and_release('tab')    

def selecaoprocessos():
    aguardar_imagem('img\\img0.png')
    pyautogui.click(492, 117, duration=0.15)
    sleep_cancelamento(timeset)
    pyautogui.click(553, 148, duration=0.15)
    sleep_cancelamento(timeset)
    pyautogui.click(1181, 813, duration=0.15)
    sleep_cancelamento(timeset + 0.5)
    pyautogui.click(568, 377, duration=0.15)
    sleep_cancelamento(timeset)
    pyautogui.click(567, 456, duration=0.15)
    sleep_cancelamento(timeset)

def cadastro_Recebimentos_materiais():
    pyautogui.click(749, 519, duration=0.15)
    sleep_cancelamento(timeset)
    pyautogui.click(1186, 817, duration=0.15)
    sleep_cancelamento(timeset)

def cadastro_Aquisição_Servico():
    pyautogui.click(757, 551, duration=0.15)
    sleep_cancelamento(timeset)
    pyautogui.click(1186, 817, duration=0.15)
    sleep_cancelamento(timeset)

def concluir_cadastro():
    pyautogui.click(1229, 819, duration=0.15) # V
    sleep_cancelamento(timeset)
    pyautogui.click(1218, 862, duration=0.15) # ULTIMA ETAPA
    sleep_cancelamento(timeset)
    pyautogui.click(1181, 813, duration=0.15) # CONCLUIR
    sleep_cancelamento(timeset)
    # pyautogui.click(1284, 816, duration=0.15) # CANCELAR
    # sleep_cancelamento(timeset)

def cadastro_Serie(cord, digito):
    pyautogui.click(1057, 353+cord, duration=0.15)
    sleep_cancelamento(timeset)
    pyautogui.click(767, 307, duration=0.15)
    sleep_cancelamento(timeset)
    pyautogui.click(1186, 815, duration=0.15)
    aguardar_imagem('img\\img2.png')
    sleep_cancelamento(timeset)
    pyautogui.click(1296, 568, duration=0.15) # }
    pyautogui.click(1296, 568, duration=0.15) # } Rolar pagina
    pyautogui.click(1296, 568, duration=0.15) # } Rolar pagina
    pyautogui.click(1296, 568, duration=0.15) # }
    sleep_cancelamento(timeset)
    pyautogui.click(1035, 558, duration=0.15)
    digitar_teclas(digito)
    sleep_cancelamento(timeset)
    concluir_cadastro()
    sleep_cancelamento(timeset)

    return cord + 19

def processo_1(id1, digito):
    if id1 >= 1 and id1 <= 6:
        id1 -= 1
    else: id1 = 7
    
    acrecenta_cordenadas = id1*19
    while id1 < 6:
        id1 += 1
        selecaoprocessos()
        cadastro_Recebimentos_materiais()
        aguardar_imagem('img\\img1.png')
        acrecenta_cordenadas = cadastro_Serie(acrecenta_cordenadas, digito)
        concluir_cadastro()
        pyautogui.click(1020, 611, duration=0.15)
        print(f'Processo 1 - Finalizado {id1} de 6')
        sleep_cancelamento(timeset+3)

def processo_2(id2, digito):
    if id2 >= 1 and id2 <= 13:
        id2 -= 1
    else: id2 = 14
    acrecenta_cordenadas = id2*19
    while id2 < 13:
        id2 += 1
        selecaoprocessos()
        cadastro_Aquisição_Servico()
        aguardar_imagem('img\\img1.png')
        acrecenta_cordenadas = cadastro_Serie(acrecenta_cordenadas, digito)
        concluir_cadastro()
        pyautogui.click(1020, 611, duration=0.15)
        print(f'Processo 2 - Finalizado {id2} de 13')
        sleep_cancelamento(timeset+3)

def main():
    print("\n" + "=" * 50)
    print("CONFIGURAÇÕES DEFINIDAS:")
    digito = input("Digite o número da série (ex: 011): ")
    id1 = int(input("Digite o ID inicial para o Processo 1 (1 a 6): "))
    id2 = int(input("Digite o ID inicial para o Processo 2 (1 a 13): "))
    processo_1(id1, digito)
    processo_2(id2, digito)
    print(f"Serie {digito} Cadastrada com sucesso!")
if __name__ == "__main__":
    main()