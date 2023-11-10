import os
import openpyxl
import pyautogui
import keyboard

os.system('cls')

PLANILHA = openpyxl.load_workbook('nota.xlsx')
PAGINA = PLANILHA['3º PERÍODO']

# Lista das colunas a serem preenchidas
# Artes, Ciencias, Educacao Fisica, Ensino Religioso, Geografia, Historia, Ingles, Lingua Portuguesa, Matematica

# colunas = ['N', 'AD', 'R', 'AH', 'AP', 'AL', 'Z', 'F', 'V']
colunas = [13, 29, 17, 33, 41, 37, 25, 5, 21]

def check_for_esc_key():
    if keyboard.is_pressed('esc'):
        print("Tecla Esc pressionada. Encerrando o script.")
        exit()

for linha in PAGINA.iter_rows(min_row=12):
    if linha[1].value is not None:
        for coluna in colunas:
            check_for_esc_key()  # Verifique se a tecla Esc foi pressionada
            valor_celula = str(linha[coluna].internal_value)
            print(valor_celula)
            # if valor_celula != "#DIV/0!":
            #     pyautogui.write(valor_celula.replace('.', ','))
            # # Se o valor for "#DIV/0!", deixe em branco
            # pyautogui.press('tab')
    else:
        break
