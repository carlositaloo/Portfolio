import os
import openpyxl
import pyautogui


os.system('cls')

PLANILHA = openpyxl.load_workbook('NOTAS.xlsx')
PAGINA = PLANILHA['9B']
pyautogui.click(661, 878, duration=0.25)
pyautogui.doubleClick(526, 112, duration=0.25)

for linha in PAGINA.iter_rows(min_row=2):
    # ARTES
    pyautogui.write(str(linha[2].value).replace('.', ','))
    pyautogui.press('tab')
    # CIENCIAS
    pyautogui.write(str(linha[6].value).replace('.', ','))
    pyautogui.press('tab')
    # EDUC.FISICA
    pyautogui.write(str(linha[3].value).replace('.', ','))
    pyautogui.press('tab')
    # ENS.RELIGIOSO
    pyautogui.write(str(linha[7].value).replace('.', ','))
    pyautogui.press('tab')
    # GEOGRAFIA
    pyautogui.write(str(linha[9].value).replace('.', ','))
    pyautogui.press('tab')
    # HISTORIA
    pyautogui.write(str(linha[8].value).replace('.', ','))
    pyautogui.press('tab')
    # INGLES
    pyautogui.write(str(linha[5].value).replace('.', ','))
    pyautogui.press('tab')
    # LING.PORTUGUESA
    pyautogui.write(str(linha[1].value).replace('.', ','))
    pyautogui.press('tab')
    # MATEMATICA
    pyautogui.write(str(linha[4].value).replace('.', ','))
    pyautogui.press('tab')
