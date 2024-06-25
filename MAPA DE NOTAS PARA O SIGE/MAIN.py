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
# pyautogui.doubleClick(564, 129, duration=0.25)
pyautogui.doubleClick(510, 126, duration=0.25)

# Lista das colunas a serem preenchidas
# ARTE,	CIENCIAS, EDUC.FISICA, ENS.RELIGI, ETIC.CIDADAN, GEOGRAFIA, HISTORIA, LING.EST.ING, LING.PORTUG, MATEMATICA, PROG INTEL, PROJETOCAMIN
# colunas = ['M', 'AE', 'S', 'AK', 'BI', 'AW', 'AQ', 'BC', 'G', 'Y', 'BO', 'BV']
colunas = [10, 28, 16, 34, 58, 46, 40, 52, 4, 22, 64, 70]

def check_for_esc_key():
    if keyboard.is_pressed('esc'):
        print("\n\nTecla Esc pressionada. Encerrando o script.\n")
        exit()

def converter_materia(colunas):
    dicionario = {10: 'Art.', 28: 'Ciên.', 16: 'E.F.', 34: 'Relig.', 58: 'É.C.', 46: 'Geo.', 40: 'His.', 52: 'Ing.', 4: 'Port.', 22: 'Mat.', 64: 'P.I.', 70: 'Proj.C.'}
    materia = {k: dicionario[k] for k in colunas}
    return materia

materias = converter_materia(colunas)
alunos = len(materias) -1
x = 0
for linha in PAGINA.iter_rows(min_row=4):
    if linha[0].value is not None:
        print(f' {" ".join(linha[0].value.split()[:2]):<20} ', end='|')
        for coluna in colunas:
            check_for_esc_key()  # Verifique se a tecla Esc foi pressionada
            valor_celula = str(linha[coluna].value)
            nome_materia = materias[coluna]
            print(f' {nome_materia}: {valor_celula:<4} ', end='|')
            x = 0 if x == alunos else x + 1; print('') if x == 0 else None
            if valor_celula != "#DIV/0!":
                pyautogui.write(valor_celula.replace('.', ','))
            # Se o valor for "#DIV/0!", deixe em branco
            pyautogui.press('tab')
    else:
        break
