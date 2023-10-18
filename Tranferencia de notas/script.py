import os
import pyperclip
import pyautogui

# python
# from mouseinfo import mouseInfo
# mouseInfo()
# F6

pyautogui.PAUSE = 0.01

# Obtém o texto do clipboard
texto = pyperclip.paste()

# Use a função split para dividir o texto em partes
valores = texto.split()
print(valores)

# Agora você pode atribuir os valores a variáveis individuais
Artes = valores[0]
Ciencias = valores[1]
Edufisica = valores[2]
Religiao = valores[3]
Geografia = valores[4]
Historia = valores[5]
Ingles = valores[6]
Portugues = valores[7]
Matematica = valores[8]

variaveis = [Portugues, Ingles, Edufisica, Artes, Matematica, Ciencias, Historia, Geografia, Religiao]

# pyautogui.click(761, 880, duration=0.25)
pyautogui.press('esc')

for c in variaveis:
    # print(c)
    pyautogui.write(str(c))
    pyautogui.press('down')
