import pyautogui
import keyboard
import pyperclip
import time
import sys

# ---------- Configurações ---------- #
ativa_questao = True
questao = "7.1"
enunciado = "Recomendaria o internato para outros estudantes."
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


def colar_texto(texto):
    """Copia e cola o texto no campo atual."""
    checar_parar()
    pyperclip.copy(texto)
    pyautogui.write('o')  # Garante que há foco
    keyboard.press_and_release('backspace')
    time.sleep(1)
    checar_parar()
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.5)


# ---------- Execução do Script ---------- #

# Abertura do navegador
checar_parar()
pyautogui.click(989, 1057, duration=tempo_click)
time.sleep(0.5)

# Adicionar questão
checar_parar()
pyautogui.click(23, 103, duration=tempo_click)
time.sleep(1)

# Adicionar matéria
checar_parar()
pyautogui.click(789, 356, duration=tempo_click)
keyboard.press_and_release('backspace')
time.sleep(0.1)
pyautogui.write('1')
time.sleep(0.1)
keyboard.press_and_release('tab')

# Tipo de prova
checar_parar()
pyautogui.click(1273, 412, duration=tempo_click)

# Questão ativa
checar_parar()
pyautogui.click(1003, 444, duration=tempo_click)

# Tipo de questão
checar_parar()
pyautogui.click(836, 457, duration=tempo_click)

# Código da questão
if ativa_questao:
    checar_parar()
    pyautogui.click(839, 407, duration=tempo_click)
    keyboard.press_and_release('backspace')
    time.sleep(0.1)
    pyautogui.write(questao)

# Enunciado
checar_parar()
pyautogui.click(591, 330, duration=tempo_click)
pyautogui.click(959, 342, duration=tempo_click)
colar_texto(enunciado)

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
    colar_texto(resposta)
    pyautogui.press('enter')
    time.sleep(0.3)

print("Script concluído.")
