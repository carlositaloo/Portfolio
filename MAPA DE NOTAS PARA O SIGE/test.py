import os
import openpyxl
import pyautogui


os.system('cls')

PLANILHA = openpyxl.load_workbook('NOTAS 6 A.xlsx')
PAGINA = PLANILHA['Planilha1']
pyautogui.click(661, 878, duration=0.25)

num1, num2 = 526, 112
for linha in PAGINA.iter_rows(min_row=2):
    pyautogui.click(num1, num2, duration=0.25)
    pyautogui.write(str(linha[1].value).replace('.', ','))
    # Aumentando os números em 10 pontos
    num2 += 18.5

num1, num2 = 610, 112
for linha in PAGINA.iter_rows(min_row=2):
    pyautogui.click(num1, num2, duration=0.25)
    pyautogui.write(str(linha[2].value).replace('.', ','))
    # Aumentando os números em 10 pontos
    num2 += 18.5

num1, num2 = 695, 112
for linha in PAGINA.iter_rows(min_row=2):
    pyautogui.click(num1, num2, duration=0.25)
    pyautogui.write(str(linha[3].value).replace('.', ','))
    # Aumentando os números em 10 pontos
    num2 += 18.5

num1, num2 = 780, 112
for linha in PAGINA.iter_rows(min_row=2):
    pyautogui.click(num1, num2, duration=0.25)
    pyautogui.write(str(linha[4].value).replace('.', ','))
    # Aumentando os números em 10 pontos
    num2 += 18.5

num1, num2 = 780, 112
for linha in PAGINA.iter_rows(min_row=2):
    pyautogui.click(num1, num2, duration=0.25)
    pyautogui.write(str(linha[5].value).replace('.', ','))
    # Aumentando os números em 10 pontos
    num2 += 18.5
