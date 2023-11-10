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
pyautogui.click(661, 878, duration=0.25)
pyautogui.click(473, 840, duration=0.25)
pyautogui.doubleClick(526, 112, duration=0.25)

# Lista das colunas a serem preenchidas
# Artes, Ciencias, Educacao Fisica, Ensino Religioso, Geografia, Historia, Ingles, Lingua Portuguesa, Matematica
# colunas = ['M', 'AC', 'Q', 'AG', 'AO', 'AK', 'Y', 'E', 'U']
colunas = [12, 28, 16, 32, 40, 36, 24, 4, 20]

def check_for_esc_key():
    if keyboard.is_pressed('esc'):
        print("Tecla Esc pressionada. Encerrando o script.")
        exit()

for linha in PAGINA.iter_rows(min_row=0):
    if linha[0].value is not None:
        for coluna in colunas:
            check_for_esc_key()  # Verifique se a tecla Esc foi pressionada
            valor_celula = str(linha[coluna].value)
            print(valor_celula)
            if valor_celula != "#DIV/0!":
                pyautogui.write(valor_celula.replace('.', ','))
            # Se o valor for "#DIV/0!", deixe em branco
            pyautogui.press('tab')
    else:
        break
