import pyautogui
import keyboard
import time
import sys

# Quantidade de vezes que o script irá rodar
NUM_EXECUCOES = 10

pyautogui.click(841, 1059, duration=0.25)

def click_com_espera(x, y, espera=1):
    """Clica nas coordenadas (x, y) com uma espera definida e verifica se a tecla ESC foi pressionada."""
    if keyboard.is_pressed('esc'):
        print("\nTecla ESC pressionada. Encerrando o script.\n")
        sys.exit()
    pyautogui.click(x, y, duration=0.25)
    time.sleep(espera)

def executar_passos():
    passos = [
        (849, 382),
        'PgDn',               # Comando especial
        (779, 525),
        (798, 809),
        (710, 877),
        (669, 957),
        (871, 925)
    ]

    for passo in passos:
        if isinstance(passo, tuple):
            click_com_espera(*passo)
        elif isinstance(passo, str):
            if keyboard.is_pressed('esc'):
                print("\nTecla ESC pressionada. Encerrando o script.\n")
                sys.exit()
            pyautogui.press(passo.lower(), interval=0.25)
            time.sleep(1)

def main():
    print(f"Iniciando automação por {NUM_EXECUCOES} vezes. Pressione ESC para cancelar a qualquer momento.")
    
    for i in range(NUM_EXECUCOES):
        print(f"\nExecução {i + 1} de {NUM_EXECUCOES}")
        executar_passos()

    print("\nAutomação finalizada.")

if __name__ == "__main__":
    main()
