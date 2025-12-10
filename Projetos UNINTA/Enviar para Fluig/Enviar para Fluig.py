import pyautogui
import pyperclip
import time
import keyboard
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import os

# Configurações iniciais
timeset = 0.1
usuario = pyperclip.paste().strip()

def perguntar_bool(pergunta="Digite True/False ou 1/0: "):
    while True:
        resposta = input(pergunta).strip().lower()
        
        if resposta in ["true", "1"]:
            return True
        elif resposta in ["false", "0"]:
            return False
        else:
            print("Entrada inválida! Digite True, False, 1 ou 0.")

# Exemplo de uso
permission = perguntar_bool("Você deseja pular a etapa de enviar GED? (True/False ou 1 - Sim / 0 - Não): ")

if not permission:  # equivale a if permission == False:
    print("Função desativada.")
else:
    print("Função ativada.")



# Correção do caminho - adicione apenas estas 2 linhas
script_dir = os.path.dirname(os.path.abspath(__file__))


def verificar_cancelamento():
    try:
        if keyboard.is_pressed('esc'):
            print("Script cancelado pelo usuário.")
            time.sleep(0.1)  # Evita múltiplas detecções
            # Verifica novamente para confirmar
            if keyboard.is_pressed('esc'):
                sys.exit()
    except Exception:
        # Continua executando se houver erro na detecção
        pass


def sleep_cancelamento(duration):
    """Sleep que verifica ESC a cada 0.1s"""
    elapsed = 0
    while elapsed < duration:
        verificar_cancelamento()
        sleep_time = min(0.1, duration - elapsed)
        time.sleep(sleep_time)
        elapsed += sleep_time


def aguardar_imagem(imagem_path, numero=1, timeout=30, intervalo=0.1, confidence=0.8):
    """
    Aguarda uma imagem aparecer na tela.
    numero: qual ocorrência da imagem retornar (1 = primeira, 2 = segunda, etc.)
    """
    caminho_completo = os.path.join(script_dir, imagem_path)
    tempo_inicial = time.time()

    while time.time() - tempo_inicial < timeout:
        verificar_cancelamento()
        try:
            todas = list(pyautogui.locateAllOnScreen(
                caminho_completo, confidence=confidence))
            if len(todas) >= numero:
                return todas[numero - 1]  # retorna a n-ésima ocorrência
        except Exception as e:
            pass
        sleep_cancelamento(intervalo)

    raise TimeoutError(
        f"Imagem {imagem_path} (ocorrência {numero}) não encontrada em {timeout}s")


if permission == False:
    img = aguardar_imagem('img\\img1.png')
    verificar_cancelamento()
    pyautogui.click(img, duration=0.15)
    img = aguardar_imagem('img\\img2.png')
    if img:  # Se achou a imagem
        x, y = pyautogui.center(img)  # pega o centro
        pyautogui.click(x, y + 50, duration=0.15)  # clica 100px abaixo
        pyautogui.write(usuario)
        time.sleep(0.2)  # espera o SO processar o comando
        pyautogui.press('enter')

    try:
        img = aguardar_imagem('img\\img10.png', timeout=3)
        if img:
            while True:
                resposta = input("Imagem encontrada! Digite 'sim' para continuar: ").strip().lower()
                if resposta == "sim":
                    break
                else:
                    print("Digite exatamente 'sim' para continuar...")
    except TimeoutError:
        img = None  # não achou a imagem, só segue sem o input

    img = aguardar_imagem('img\\img3.png')
    pyautogui.click(img, duration=0.15)
    pyautogui.hotkey('ctrl', 'p')
    img = aguardar_imagem('img\\img4.png')
    pyautogui.click(img, duration=0.15)

    aguardar_imagem('img\\img5.png')
    img = aguardar_imagem('img\\img6.png')
    pyautogui.click(img, duration=0.15)
    img = aguardar_imagem('img\\img7.png')
    pyautogui.click(img, duration=0.15)
    img = aguardar_imagem('img\\img8.png')
    pyautogui.click(img, duration=0.15)
    img = aguardar_imagem('img\\img9.png')
    pyautogui.click(img, duration=0.15)

options = webdriver.ChromeOptions()
options.add_argument('--headless=new')
navegador = webdriver.Chrome(options=options)
navegador.get('https://fluig.aiamis.com.br/portal/p/01/wcmuserpage')
navegador.maximize_window()

navegador.find_element("id", "username").send_keys("1-07337")
navegador.find_element("id", "password").send_keys("catucada1")
navegador.find_element("id", "submitLogin").click()

navegador.find_element("id", "wcm-datatable-textSearch-wcmid4").send_keys(usuario)
WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.ID, f"jqg_wcmid4_{usuario}")))
navegador.find_element("id", f"jqg_wcmid4_{usuario}").click()
navegador.find_element("xpath", "//a[@title='Editar']").click()
WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.ID, "btnGroups")))
navegador.find_element("id", "btnGroups").click()
WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'datatable-buttonsEventFunction-ecm-usergroup-table') and @title='Adicionar']")))
navegador.find_element("xpath", "//a[contains(@class, 'datatable-buttonsEventFunction-ecm-usergroup-table') and @title='Adicionar']").click()
navegador.find_element("id", "wcm-datatable-textSearch-ecm-usergroupzoom-table").send_keys("automacao")
WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.ID, "jqg_ecm-usergroupzoom-table_AUTOMACAOPONTO")))
navegador.find_element("id", "jqg_ecm-usergroupzoom-table_AUTOMACAOPONTO").click()

navegador.find_element("id", "panel-button-wcmid19-0").click()
navegador.find_element("id", "panel-button-wcmid14-0").click()
navegador.find_element("id", "panel-button-wcmid9-0").click()

os.system("cls")
print("\n\nFinalizado!!!\n\n")