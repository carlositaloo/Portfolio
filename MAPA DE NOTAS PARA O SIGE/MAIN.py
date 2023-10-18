import os
import openpyxl
import pyautogui

# python
# from mouseinfo import mouseInfo
# mouseInfo()
# F6

os.system('cls')

PLANILHA = openpyxl.load_workbook('NOTAS.xlsx')
PAGINA = PLANILHA['9B']
pyautogui.click(661, 878, duration=0.25)
pyautogui.doubleClick(526, 112, duration=0.25)

# Lista das colunas a serem preenchidas
# Artes, Ciencias, Educacao Fisica, Ensino Religioso, Geografia, Historia, Ingles, Lingua Portuguesa, Matematica
colunas = [2, 6, 3, 7, 9, 8, 5, 1, 4]

for linha in PAGINA.iter_rows(min_row=2):
    for coluna in colunas:
        pyautogui.write(str(linha[coluna].value).replace('.', ','))
        pyautogui.press('tab')
