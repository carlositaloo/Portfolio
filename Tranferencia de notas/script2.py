import pyperclip
import pyautogui

pyautogui.PAUSE = 0.01

# Obtém o texto do clipboard e divide em valores
texto = pyperclip.paste()
valores = texto.split()
print(valores)

# Cria listas de variáveis para cada período
Artes, Ciencias, Edufisica, Religiao, Geografia, Historia, Ingles, Portugues, Matematica = ([
] for _ in range(9))

# Distribui os valores pelas listas
for i in range(0, len(valores), 9):
    Artes.append(valores[i])
    Ciencias.append(valores[i + 1])
    Edufisica.append(valores[i + 2])
    Religiao.append(valores[i + 3])
    Geografia.append(valores[i + 4])
    Historia.append(valores[i + 5])
    Ingles.append(valores[i + 6])
    Portugues.append(valores[i + 7])
    Matematica.append(valores[i + 8])

# for i in range(0, len(valores), 9):
#     Portugues.append(valores[i])
#     Artes.append(valores[i + 1])
#     Edufisica.append(valores[i + 2])
#     Ingles.append(valores[i + 3])
#     Historia.append(valores[i + 4])
#     Geografia.append(valores[i + 5])
#     Religiao.append(valores[i + 6])
#     Ciencias.append(valores[i + 7])
#     Matematica.append(valores[i + 8])

# Organiza as notas por período
periodos = [
    [Portugues[0], Matematica[0], Historia[0], Geografia[0],
        Ciencias[0], Artes[0], Religiao[0], Ingles[0], Edufisica[0]],
    [Portugues[1], Matematica[1], Historia[1], Geografia[1],
        Ciencias[1], Artes[1], Religiao[1], Ingles[1], Edufisica[1]],
    [Portugues[2], Matematica[2], Historia[2], Geografia[2],
        Ciencias[2], Artes[2], Religiao[2], Ingles[2], Edufisica[2]]
]
pyautogui.press('esc')
# Inserir notas para cada período
for periodo in periodos:
    for nota in periodo:
        pyautogui.write(str(nota).replace('.', ','))
        pyautogui.press('down')
    pyautogui.press('right')
    pyautogui.press('up', presses=9)


