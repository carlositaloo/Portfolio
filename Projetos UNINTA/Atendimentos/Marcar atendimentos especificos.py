import pyautogui
import keyboard
import pyperclip
import time
import sys

# === CONFIGURAÇÕES ===
# IDs de atendimento
IDS = [
    "1-1-65194",
    "1-1-65878",
    "1-1-96274",
    "1-1-103507",
    "1-1-103521",
    "1-1-103732",
    "1-1-103738",
    "1-1-103740",
    "1-1-103741",
    "1-1-103806",
    "1-1-103808",
    "1-1-103823",
    "1-1-105430",
    "1-1-105447",
    "1-1-105646",
    "1-1-105871",
    "1-1-106032",
    "1-1-106448",
    "1-1-107345",
    "1-1-108793",
    "1-1-110020",
    "1-1-655497"
]

# Variável global para controlar a execução
should_stop = False

def on_esc():
    global should_stop
    print("\n< ESC pressionado — script será encerrado após a operação atual >")
    should_stop = True

def main():
    global should_stop
    
    # Registra o hotkey do ESC apenas UMA vez
    keyboard.add_hotkey('esc', on_esc)
    
    print("Script iniciado. Pressione ESC para interromper.")
    print(f"Processando {len(IDS)} IDs...")
    
    # pyautogui.hotkey('alt', 'tab') # Alterar janela se necessário
    time.sleep(1)  # Tempo para focar na janela
    
    for i, atendimento_id in enumerate(IDS, 1):
        # Verifica se deve parar
        if should_stop:
            print(f"\n< Script interrompido no item {i}/{len(IDS)} >")
            break
            
        print(f"Processando {i}/{len(IDS)}: {atendimento_id}")
        
        try:
            # Copia o ID para o clipboard
            pyperclip.copy(atendimento_id)
            
            # Clica no campo de pesquisa
            pyautogui.doubleClick(1762, 174, duration=0.25)
            
            # Verifica novamente se deve parar
            if should_stop:
                break
                
            # Cola o ID do atendimento
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(1.5)
            
            # Verifica novamente se deve parar
            if should_stop:
                break
                
            # Seleciona o primeiro resultado
            pyautogui.click(114, 325, duration=0.25)
            
            # Pequena pausa entre operações
            time.sleep(0.5)
            
        except Exception as e:
            print(f"Erro ao processar {atendimento_id}: {e}")
            continue
    
    if not should_stop:
        print("\n< Processo concluído com sucesso >")
    
    # Remove o hotkey antes de sair
    keyboard.remove_all_hotkeys()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n< Script interrompido pelo usuário (Ctrl+C) >")
    except Exception as e:
        print(f"\n!! Erro inesperado: {e}")
    finally:
        # Garante que os hotkeys sejam removidos
        keyboard.remove_all_hotkeys()
        sys.exit(0)