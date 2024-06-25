import os
import openpyxl
import pyautogui
import keyboard

# python
# from mouseinfo import mouseInfo
# mouseInfo()
# F6

os.system('cls')

PLANILHA = openpyxl.load_workbook('NOTAS.xlsx')
PAGINA = PLANILHA['NOTAS']
pyautogui.click(706, 884, duration=0.25)
pyautogui.doubleClick(567, 126, duration=0.25)

# Lista das colunas a serem preenchidas
# ARTE,	CIENCIAS, EDUC.FISICA, ENS.RELIGI, ETIC.CIDADAN, GEOGRAFIA, HISTORIA, LING.EST.ING, LING.PORTUG, MATEMATICA, PROG INTEL
# colunas = ['M', 'AE', 'S', 'AK', 'BI', 'AW', 'AQ', 'BC', 'G', 'Y', 'BO']
colunas = [12, 30, 18, 36, 60, 48, 42, 54, 6, 24, 66]

def check_for_esc_key():
    if keyboard.is_pressed('esc'):
        print("\n\nTecla Esc pressionada. Encerrando o script.\n")
        exit()

def converter_materia(colunas):
    dicionario = {12: 'Art.', 30: 'Ciên.', 18: 'E.F.', 36: 'Relig.', 60: 'É.C.', 48: 'Geo.', 42: 'His.', 54: 'Ing.', 6: 'Port.', 24: 'Mat.', 66: 'P.I.'}
    materia = {k: dicionario[k] for k in colunas}
    return materia

materias = converter_materia(colunas)
x = 0
for linha in PAGINA.iter_rows(min_row=4):
    if linha[0].value is not None:
        print(f' {" ".join(linha[0].value.split()[:2]):<18} ', end='|')
        for coluna in colunas:
            check_for_esc_key()  # Verifique se a tecla Esc foi pressionada
            valor_celula = str(linha[coluna].value)
            nome_materia = materias[coluna]
            print(f' {nome_materia}: {valor_celula:<4} ', end='|')
            x = 0 if x == 10 else x + 1; print('') if x == 0 else None
            if valor_celula != "#DIV/0!":
                pyautogui.write(valor_celula.replace('.', ','))
            # Se o valor for "#DIV/0!", deixe em branco
            pyautogui.press('tab')
    else:
        break
