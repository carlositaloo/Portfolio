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

pyautogui.click(689, 884, duration=0.25) #Navegador
pyautogui.doubleClick(16, 109, duration=0.25)
pyautogui.press('tab')

# CONFIGURAÇÕES:
projetocamin = True # Coloque True para 8º e 9º anos
adicionarcoluna = 0 # Use 2 para med
# Lista das colunas a serem preenchidas
Lista = {10: 'Art.', 28: 'Ciên.', 16: 'E.F.', 34: 'Relig.', 58: 'É.C.', 46: 'Geo.', 40: 'His.', 52: 'Ing.', 4: 'Port.', 22: 'Mat.', 67: 'P.I.', 70: 'Proj.C.'}

Lista = {key + adicionarcoluna: value for key, value in Lista.items()}

colunas = list(Lista.keys())
if projetocamin == False:
    colunas.pop()  # Remove a última chave

def check_for_esc_key():
    if keyboard.is_pressed('esc'):
        print("\n\nTecla Esc pressionada. Encerrando o script.\n")
        exit()

def converter_materia(colunas):
    dicionario = Lista.copy()
    materia = {k: dicionario[k] for k in colunas}
    return materia

materias = converter_materia(colunas)
x = 0
contador = 1  # Inicia o contador
for linha in PAGINA.iter_rows(min_row=5):
    if linha[0].value is not None:
        print(f'|{contador:>2}| {" ".join(linha[0].value.split()[:2]):<20} ', end='|')
        contador += 1  # Incrementa o contador
        for coluna in colunas:
            check_for_esc_key()  # Verifique se a tecla Esc foi pressionada
            valor_celula = str(linha[coluna].value)
            nome_materia = materias[coluna]
            print(f' {nome_materia}: {valor_celula:<4} ', end='|')
            x = 0 if x == len(materias.keys()) -1 else x + 1
            print('') if x == 0 else None
            if valor_celula != "#DIV/0!":
                pyautogui.write(valor_celula.replace('.', ','))
            # Se o valor for "#DIV/0!", deixe em branco
            pyautogui.press('tab')
    else:
        break
