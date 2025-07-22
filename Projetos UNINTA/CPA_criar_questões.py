import pyautogui
import keyboard
import pyperclip
import time
import sys

# ---------- Configurações ---------- #
tempo_click = 0.3  # Duração de cada clique

respostas = [
    "Discordo totalmente",
    "Discordo",
    "Discordo parcialmente",
    "Concordo parcialmente",
    "Concordo",
    "Concordo totalmente",
    "Não sei responder",
    "Não se aplica"
]


def checar_parar():
    """Interrompe o script se a tecla ESC for pressionada."""
    if keyboard.is_pressed('esc'):
        print("Script interrompido pelo usuário.")
        sys.exit()


def digitar_com_checar(texto):
    """Copia e cola o texto no campo atual."""
    checar_parar()
    pyperclip.copy(texto)
    pyautogui.write('o')  # Garante que há foco
    keyboard.press_and_release('backspace')
    time.sleep(1)
    checar_parar()
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.5)


# Navegador
checar_parar()
pyautogui.click(989, 1057, duration=0.25)
time.sleep(0.5)

# Adicionar resposta
checar_parar()
pyautogui.click(753, 428, duration=tempo_click)

# Número de alternativas (inicial)
checar_parar()
pyautogui.click(843, 516, clicks=2, interval=0.1, duration=tempo_click)
keyboard.press_and_release('backspace')
time.sleep(0.1)
pyautogui.write('1')

# Adicionar mais 7 alternativas
for _ in range(7):
    checar_parar()
    pyautogui.click(753, 428, duration=tempo_click)
    time.sleep(0.3)

# Campo de alternativas
checar_parar()
pyautogui.click(1078, 516, duration=tempo_click)

# Preencher alternativas
for resposta in respostas:
    checar_parar()
    digitar_com_checar(resposta)
    pyautogui.press('enter')
    time.sleep(0.3)

print("Script concluído.")
