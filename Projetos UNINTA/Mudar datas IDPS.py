import pyautogui
import keyboard
import pyperclip
import time
import sys

# Lista com os textos que você quer copiar e colar
IDPS = ["1562", "1563", "1564", "1565", "1566"]
indice = 0  # Começa no primeiro item da lista

def on_esc():
    print("\n< ESC pressionado — script encerrado >")
    sys.exit(0)


pyautogui.click(1035, 1060, duration=0.25)
keyboard.add_hotkey('esc', on_esc)

while indice < len(IDPS):
    pyautogui.click(629, 203, duration=0.25)
    keyboard.add_hotkey('esc', on_esc)

    texto = IDPS[indice]
    pyperclip.copy(texto)  # Copia para a área de transferência
    pyautogui.hotkey("ctrl", "v")  # Cola
    indice += 1  # Avança para o próximo item
    time.sleep(0.5)  # Pequena pausa para evitar múltiplos envios
    keyboard.add_hotkey('esc', on_esc)
    pyautogui.press("enter")
    time.sleep(3)
    keyboard.add_hotkey('esc', on_esc)

    pyautogui.doubleClick(302, 308, duration=0.25)
    time.sleep(4)
    keyboard.add_hotkey('esc', on_esc)
    pyautogui.click(794, 254, duration=0.25)
    keyboard.add_hotkey('esc', on_esc)
    pyautogui.click(841, 320, duration=0.25)
    keyboard.add_hotkey('esc', on_esc)
    pyperclip.copy("03/08/2025 00:01")  # Copia para a área de transferência
    pyautogui.hotkey("ctrl", "a")
    keyboard.add_hotkey('esc', on_esc)
    pyautogui.hotkey("ctrl", "v")

    pyautogui.click(837, 399, duration=0.25)
    keyboard.add_hotkey('esc', on_esc)
    pyautogui.hotkey("ctrl", "a")
    keyboard.add_hotkey('esc', on_esc)
    pyautogui.hotkey("ctrl", "v") 
    pyautogui.click(1262, 841, duration=0.25)
    time.sleep(3)
    keyboard.add_hotkey('esc', on_esc)