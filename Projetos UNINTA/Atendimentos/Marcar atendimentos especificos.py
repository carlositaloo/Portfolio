import pyautogui
import keyboard
import pyperclip
import time
import sys
import os

# === CONFIGURAÇÕES ===
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# IDs de atendimento
IDS = [
    # "1-1-1383409",
    "1-1-1385822",
    "1-1-1386539",
    "1-1-1422113",
    "1-1-1391634",
    "1-1-1393745",
    "1-1-1394044",
    "1-1-1394050",
    "1-1-1394111",
    "1-1-1394230",
    "1-1-1395490",
    "1-1-1418101",
    "1-1-1401341",
    "1-1-1401698",
    "1-1-1402488",
    "1-1-1396338",
    "1-1-1399352",
    "1-1-1400261",
    "1-1-1400612",
    # "1-1-1382632",
    "1-1-1387092",
    "1-1-1390552",
    "1-1-1419514",
    "1-1-1422190",
    "1-1-1422257",
    "1-1-1392297",
    "1-1-1401098",
    "1-1-1401711",
    "1-1-1401888",
    "1-1-1402129",
    "1-1-1402306",
    "1-1-1402547",
    "1-1-1406531",
    "1-1-1406946",
    "1-1-1397065",
    "1-1-1399902",
    "1-1-1399957",
    "1-1-1400198",
    "1-1-1412037",
    "1-1-1412043",
    # "1-1-1382653",
    "1-1-1387748",
    "1-1-1387922",
    "1-1-1422053",
    "1-1-1393831",
    "1-1-1393895",
    "1-1-1394197",
    "1-1-1394670",
    "1-1-1394856",
    "1-1-1395765",
    "1-1-1416720",
    "1-1-1396549",
    "1-1-1411836",
    "1-1-1413343",
    "1-1-1383422",
    "1-1-1386442",
    "1-1-1386857",
    "1-1-1386921",
    "1-1-1387043",
    "1-1-1389359",
    "1-1-1422242",
    "1-1-1394362",
    "1-1-1394719",
    "1-1-1395814",
    "1-1-1401659",
    "1-1-1401775",
    "1-1-1402016",
    "1-1-1402507",
    "1-1-1398517",
    # "1-1-1381951",
    "1-1-1385807",
    "1-1-1386713",
    "1-1-1388971",
    "1-1-1389996",
    "1-1-1390536",
    "1-1-1422238",
    "1-1-1392229",
    "1-1-1394154",
    "1-1-1394764",
    "1-1-1416731",
    "1-1-1400792",
    "1-1-1401271",
    "1-1-1401332",
    "1-1-1400429",
    "1-1-1400661",
    "1-1-1413357",
    "1-1-1387568",
    "1-1-1387812",
    "1-1-1388956",
    "1-1-1390103",
    "1-1-1390469",
    "1-1-1422282",
    "1-1-1392156",
    "1-1-1393904",
    "1-1-1400835",
    "1-1-1402287",
    "1-1-1396131",
    "1-1-1399386",
    "1-1-1400530"
]

def check_esc():
    """Verifica se ESC foi pressionado"""
    if keyboard.is_pressed('esc'):
        print("\nScript cancelado pelo usuário.")
        sys.exit(0)

def wait_for_image(image_path, timeout=5, confidence=0.99):
    """Aguarda uma imagem aparecer na tela"""
    full_path = os.path.join(SCRIPT_DIR, image_path)
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        check_esc()
        try:
            location = pyautogui.locateOnScreen(full_path, confidence=confidence)
            if location:
                return location
        except pyautogui.ImageNotFoundException:
            pass
        time.sleep(0.1)
    
    raise TimeoutError(f"Imagem {image_path} não encontrada em {timeout}s")

def process_id(atendimento_id, index, total):
    """Processa um ID de atendimento"""
    print(f"Processando {index}/{total}: {atendimento_id}")
    
    try:
        # Copia ID para clipboard e clica no campo de pesquisa
        pyperclip.copy(atendimento_id)
        pyautogui.click(372, 94, duration=0.15)
        
        # Cola o ID
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.click(424, 95, duration=0.15)
        
        # Verifica se encontrou resultado
        try:
            wait_for_image('img2\\img1.png')
            pyautogui.click(68, 249, duration=0.15)
            time.sleep(0.2)
        except TimeoutError:
            # wait_for_image('img2\\img0.png')
            while True:
                resposta = input("Digite 'yes' para continuar: ").strip().lower()
                if resposta == 'yes':
                    break
                else:
                    print("Resposta inválida. Digite 'yes' para continuar.")
            
    except Exception as e:
        print(f"Erro ao processar {atendimento_id}: {e}")

def main():
    print("Script iniciado. Pressione ESC para interromper.")
    print(f"Processando {len(IDS)} IDs...")
    
    time.sleep(1)  # Tempo para focar na janela
    
    try:
        for i, atendimento_id in enumerate(IDS, 1):
            check_esc()
            process_id(atendimento_id, i, len(IDS))
            
        print("\n< Processo concluído com sucesso >")
        
    except KeyboardInterrupt:
        print("\n< Script interrompido pelo usuário >")
    except Exception as e:
        print(f"\n!! Erro inesperado: {e}")

if __name__ == "__main__":
    main()