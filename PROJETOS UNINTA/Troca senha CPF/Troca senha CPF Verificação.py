import pyautogui
import time
import keyboard
import pyperclip
import sys
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
from playwright.sync_api import Playwright, sync_playwright, expect

# Carrega o .env da pasta Documents do usuário atual
env_path = os.path.join(os.path.expanduser('~'), 'Documents', '.env')
load_dotenv(env_path)

usuario = pyperclip.paste().strip()
script_dir = os.path.dirname(os.path.abspath(__file__))


def consultaBanco(sql):
    user = os.getenv("DB_USER")
    password = quote_plus(os.getenv("DB_PASSWORD"))
    server = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    database = os.getenv("DB_NAME")
    driver = quote_plus("ODBC Driver 18 for SQL Server")

    engine = create_engine(
        f"mssql+pyodbc://{user}:{password}@{server}:{port}/{database}"
        f"?driver={driver}"
        "&Encrypt=no"
        "&TrustServerCertificate=yes"
    )

    cpf = ""
    nome = ""
    colaborador = ""
    with engine.connect() as conn:
        result = conn.execute(text(sql))
        
        for row in result:
            nome = row[1]
            cpf = row[2]
            colaborador = row[4]
    return cpf, nome, colaborador


def verificar_cancelamento():
    """Cancela o script se ESC for pressionado"""
    try:
        if keyboard.is_pressed('esc'):
            print("Script cancelado pelo usuário.")
            time.sleep(0.1)  # evita múltiplas detecções
            if keyboard.is_pressed('esc'):
                sys.exit()
    except Exception:
        pass

def sleep_cancelamento(duration):
    """Sleep com verificação de cancelamento"""
    elapsed = 0
    while elapsed < duration:
        verificar_cancelamento()
        sleep_time = min(0.1, duration - elapsed)
        time.sleep(sleep_time)
        elapsed += sleep_time

def aguardar_imagem(imagem_path, timeout=30, intervalo=0.1, confidence=0.9, continuar=False, click='center'):
    """Aguarda uma imagem aparecer na tela e retorna a posição para clicar"""
    caminho_completo = os.path.join(script_dir, imagem_path)
    inicio = time.time()
    while time.time() - inicio < timeout:
        verificar_cancelamento()
        try:
            posicao = pyautogui.locateOnScreen(caminho_completo, confidence=confidence)
            if posicao:
                x, y, largura, altura = posicao
                
                pontos_click = {
                    'center': (x + largura // 2, y + altura // 2),
                    'right': (x + largura, y + altura // 2),
                    'left': (x, y + altura // 2),
                    'top': (x + largura // 2, y),
                    'bot': (x + largura // 2, y + altura),
                    'topleft': (x, y),
                    'topright': (x + largura, y),
                    'botleft': (x, y + altura),
                    'botright': (x + largura, y + altura)
                }
                
                return pontos_click.get(click, pontos_click['center'])
        except Exception:
            pass
        sleep_cancelamento(intervalo)
    if continuar:
        return None
    else:
        raise TimeoutError(f"Imagem {imagem_path} não encontrada em {timeout}s")

def clicar(posicao, duration=0.15, clicks=1, interval=0.0):
    """Clique com verificação de cancelamento"""
    verificar_cancelamento()
    pyautogui.click(posicao, clicks=clicks, interval=interval, duration=duration)
    sleep_cancelamento(0.1)

def escrever(texto, intervalo=0.05):
    """Escreve texto simulando teclado"""
    verificar_cancelamento()
    pyautogui.write(texto, interval=intervalo)
    sleep_cancelamento(0.1)



sql = f"""
SELECT 
    PPESSOA.CODUSUARIO AS USUARIO,
    PPESSOA.NOME,
    PPESSOA.CPF,
    SALUNO.RA,
    PFUNC.CODSITUACAO AS STATUS_COLABORADOR
FROM PPESSOA WITH (NOLOCK)
LEFT JOIN SALUNO WITH (NOLOCK)
    ON SALUNO.CODPESSOA = PPESSOA.CODIGO
LEFT JOIN (
    SELECT 
        CODPESSOA,
        CODSITUACAO,
        ROW_NUMBER() OVER (PARTITION BY CODPESSOA ORDER BY CASE WHEN CODSITUACAO = 'A' THEN 0 ELSE 1 END) AS RN
    FROM PFUNC WITH (NOLOCK)
) PFUNC
    ON PFUNC.CODPESSOA = PPESSOA.CODIGO 
    AND PFUNC.RN = 1
WHERE PPESSOA.CODUSUARIO = '{usuario}'
"""

cpf, nome, colaborador = consultaBanco(sql)
print(f"Usuario: {usuario}\nNome do usuário: {nome}\nCPF do usuário: {cpf}\n")


aguardar_imagem('img\\usuario.png')

botao_por_usuario = aguardar_imagem('img\\porusuario.png', timeout=2, continuar=True)
if not botao_por_usuario:
    botao_por_usuario = aguardar_imagem('img\\porusuario1.png')
clicar(botao_por_usuario)
aguardar_imagem('img\\filtro.png')
escrever(usuario)
pyautogui.press('enter')
seletor = aguardar_imagem('img\\select.png')
clicar((seletor[0] + 300, seletor[1] + 30), clicks=2)
if aguardar_imagem('img\\senha_login.png', timeout=2, confidence=0.99, continuar=True):
    clicar(aguardar_imagem('img\\senha_login.png'))
clicar(aguardar_imagem('img\\trocaSenha.png'))
aguardar_imagem('img\\alterar_senha.png')
escrever(cpf)
pyautogui.press('tab')
escrever(cpf)
pyautogui.press('enter')
clicar(aguardar_imagem('img\\ok.png'))

input("Pressione Enter após alterar a senha para continuar...")
cpf = 'catucada1'


link = "https://academico.aiamis.com.br/FrameHTML/web/app/RH/PortalMeuRH/#/login" if colaborador == 'A' else "https://academico.aiamis.com.br/FrameHTML/web/app/edu/portaleducacional/login/"


def aluno(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto(link)
    page.get_by_role("textbox", name="user.svg Usuário").click()
    page.get_by_role("textbox", name="user.svg Usuário").fill(usuario)
    page.get_by_role("textbox", name="user.svg Usuário").press("Tab")
    page.get_by_role("textbox", name="senha.svg Senha").fill(cpf)
    page.get_by_role("button", name="Acessar").click()
    page.goto("https://academico.aiamis.com.br/FrameHTML/web/app/edu/PortalEducacional/#/")
    page.get_by_text("Alterar Curso").click()
    page.get_by_role("radio").check()
    page.get_by_role("button", name="Confirmar").click()

    # ---------------------
    context.close()
    browser.close()


def funcionario(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto(link)
    page.get_by_role("textbox", name="Informe o seu usuário").click()
    page.get_by_role("textbox", name="Informe o seu usuário").fill(usuario)
    page.get_by_role("textbox", name="Informe o seu usuário").press("Tab")
    page.get_by_role("textbox", name="Informe sua senha").fill(cpf)
    page.get_by_role("button", name="Entrar").click()
    page.get_by_label("Ponto", exact=True).click()
    page.get_by_role("menuitem", name="Espelho de ponto").click()

    # ---------------------
    context.close()
    browser.close()

if colaborador == 'A':
    with sync_playwright() as playwright:
        funcionario(playwright)
else:
    with sync_playwright() as playwright:
        aluno(playwright)

mensagem = f"""
A senha do usuário {usuario} {nome} foi redefinida para o CPF do mesmo (somente números). Ao acessar pela primeira vez, será solicitado que altere a senha:

• No primeiro campo, insira a senha atual (CPF do usuário).
• Nos campos seguintes, digite a nova senha e confirme.
Através do link: {link}
"""

pyperclip.copy(mensagem)
print(mensagem)

input("Pressione Enter para finalizar...")