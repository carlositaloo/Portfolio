import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
from playwright.sync_api import sync_playwright, Page
from multiprocessing import Process
import time


env_path = os.path.join(os.path.expanduser('~'), 'Documents', '.env')
load_dotenv(env_path)

MODO_TESTE = False  # True = fecha o modal sem desativar | False = confirma a desativação


def buscar_desligados():
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

    sql = '''
    SELECT DISTINCT
      PFUNC.CODPESSOA,
      PFUNC.NOME
    FROM PFUNC WITH (NOLOCK)
    WHERE PFUNC.CODCOLIGADA = 1
      AND PFUNC.CODSITUACAO = 'D'
      AND NOT EXISTS (
          SELECT 1
          FROM PFUNC ATIVO WITH (NOLOCK)
          WHERE ATIVO.CODPESSOA = PFUNC.CODPESSOA
              AND ATIVO.CODSITUACAO <> 'D'
      )
    ORDER BY PFUNC.NOME
    '''

    desligados = []
    with engine.connect() as conn:
        result = conn.execute(text(sql))
        for row in result:
            desligados.append(row[1])
    return desligados


def carregar_consultados():
    if not os.path.exists("consultados.txt"):
        return set()
    with open("consultados.txt", "r", encoding="utf-8") as f:
        return set(linha.strip() for linha in f.readlines())


def salvar_consultado(nome):
    with open("consultados.txt", "a", encoding="utf-8") as f:
        f.write(f"{nome}\n")


def filtrar_novos_desligados(desligados):
    consultados = carregar_consultados()
    novos = [nome for nome in desligados if nome not in consultados]

    print(f"Total de desligados: {len(desligados)}")
    print(f"Já consultados: {len(consultados)}")
    print(f"Novos para processar: {len(novos)}")

    return novos


def acessar_fluig(page: Page):
    page.get_by_role("textbox", name="Digite seu login").fill("automacao.desligamentos")
    page.get_by_role("textbox", name="Digite sua senha").fill("G0rdinhoM@gro")
    page.get_by_role("button", name="Acessar").click()

    # Fecha modal "Status do Servidor" (botão ×) se aparecer
    try:
        page.locator("button.close[data-dismiss='modal']").click(timeout=5000)
    except Exception:
        pass

    page.locator("#wcm-datatable-textSearch-wcmid4").wait_for(state="visible", timeout=30000)


def processar_usuario(page: Page, nome: str):
    search_box = page.locator("#wcm-datatable-textSearch-wcmid4")
    search_box.click()
    search_box.fill("")  # limpa campo antes de digitar
    search_box.press_sequentially(nome, delay=50)  # digita caractere a caractere
    page.wait_for_timeout(800)  # jqGrid filtra via AJAX

    linhas_com_erro = set()

    while True:
        linhas = page.locator("#wcmid4 tbody tr:not(.jqgfirstrow)").all()
        usuario_ativo_encontrado = False
        processou_com_sucesso = False

        for idx, linha in enumerate(linhas):
            if idx in linhas_com_erro:
                continue

            status = linha.locator("td[aria-describedby='wcmid4_state']").inner_text()
            if status != "ATIVO":
                continue

            usuario_ativo_encontrado = True
            linha.locator("input[type='checkbox']").click()
            page.locator("a.datatable-buttonsEventFunction-wcmid4[data-key='2']").click()

            confirmar = page.locator("button.wcm-panel-bt-custom")
            confirmar.wait_for(state="visible", timeout=5000)

            if MODO_TESTE:
                page.locator("button.wcm-panel-bt-close").click()
                page.wait_for_timeout(500)
                for cb in page.locator(
                    "#wcmid4 tbody tr:not(.jqgfirstrow) input[type='checkbox']:checked"
                ).all():
                    cb.click()
                linhas_com_erro.add(idx)
                continue

            confirmar.click()
            page.wait_for_timeout(1000)  # aguarda processamento no servidor

            if page.locator(".wcm-panel-title:has-text('Erro')").is_visible():
                page.locator("button.wcm-panel-bt-close").click()
                page.wait_for_timeout(500)
                for cb in page.locator(
                    "#wcmid4 tbody tr:not(.jqgfirstrow) input[type='checkbox']:checked"
                ).all():
                    cb.click()
                linhas_com_erro.add(idx)
                continue

            linhas_com_erro = {i - 1 if i > idx else i for i in linhas_com_erro}
            processou_com_sucesso = True
            break

        if not usuario_ativo_encontrado or (usuario_ativo_encontrado and not processou_com_sucesso):
            break


def processar_navegador(nomes: list, auth_path: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state=auth_path)
        page = context.new_page()
        page.goto("https://fluig.aiamis.com.br/portal/p/01/wcmuserpage")

        # Fecha modal "Status do Servidor" se aparecer ao restaurar sessão
        try:
            page.locator("button.close[data-dismiss='modal']").click(timeout=5000)
        except Exception:
            pass

        page.locator("#wcm-datatable-textSearch-wcmid4").wait_for(state="visible", timeout=30000)

        for nome in nomes:
            try:
                processar_usuario(page, nome)
            except Exception as e:
                print(f"Erro ao processar {nome}: {str(e)}")
            finally:
                salvar_consultado(nome)

        context.close()
        browser.close()


if __name__ == "__main__":
    todos_desligados = buscar_desligados()
    desligados = filtrar_novos_desligados(todos_desligados)

    if not desligados:
        print("Nenhum novo funcionário para processar!")
    else:
        QUANTIDADE_NAVEGADORES = 7

        # Faz login uma única vez e salva a sessão para reuso
        auth_path = os.path.join(os.path.expanduser('~'), 'Documents', 'fluig_auth.json')
        print("Fazendo login no Fluig...")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            page.goto("https://fluig.aiamis.com.br/portal/p/01/wcmuserpage")
            acessar_fluig(page)
            context.storage_state(path=auth_path)
            context.close()
            browser.close()
        print("Sessão salva. Iniciando navegadores...")

        k, m = divmod(len(desligados), QUANTIDADE_NAVEGADORES)
        lista_nomes = [desligados[i*k + min(i, m):(i+1)*k + min(i+1, m)] for i in range(QUANTIDADE_NAVEGADORES)]

        for i, nomes in enumerate(lista_nomes):
            print(f"Navegador {i+1} processará {len(nomes)} nomes")

        processos = []
        for nomes in lista_nomes:
            if nomes:
                p = Process(target=processar_navegador, args=(nomes, auth_path))
                p.start()
                processos.append(p)
                time.sleep(2)

        for p in processos:
            p.join()

        print("Processamento concluído!")
