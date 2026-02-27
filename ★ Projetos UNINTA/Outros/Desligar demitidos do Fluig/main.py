import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
from navegador import iniciar_navegador
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from multiprocessing import Process
import time


# Carrega o .env da pasta Documents do usuário atual
env_path = os.path.join(os.path.expanduser('~'), 'Documents', '.env')
load_dotenv(env_path)

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
      JOIN PPESSOA WITH (NOLOCK)
          ON PPESSOA.CODIGO = PFUNC.CODPESSOA
    WHERE PFUNC.CODCOLIGADA = 1
      AND PFUNC.CODSITUACAO = 'D'    
      AND NOT EXISTS (
          SELECT 1
          FROM PFUNC FUNCIONARIOATIVO WITH (NOLOCK)
          WHERE FUNCIONARIOATIVO.CODPESSOA = PFUNC.CODPESSOA
              AND FUNCIONARIOATIVO.CODCOLIGADA = PFUNC.CODCOLIGADA
              AND FUNCIONARIOATIVO.CODSITUACAO <> 'D'
      )
    ORDER BY NOME
    '''

    desligados = []
    with engine.connect() as conn:
        result = conn.execute(text(sql))
        
        for row in result:
            desligados.append(row[1])
    return desligados

def carregar_consultados():
    """Carrega a lista de nomes já consultados do arquivo"""
    if not os.path.exists("consultados.txt"):
        return set()
    
    with open("consultados.txt", "r", encoding="utf-8") as f:
        return set(linha.strip() for linha in f.readlines())

def salvar_consultado(nome):
    """Adiciona um nome ao arquivo de consultados"""
    with open("consultados.txt", "a", encoding="utf-8") as f:
        f.write(f"{nome}\n")

def filtrar_novos_desligados(desligados):
    """Retorna apenas os nomes que ainda não foram consultados"""
    consultados = carregar_consultados()
    novos = [nome for nome in desligados if nome not in consultados]
    
    print(f"Total de desligados: {len(desligados)}")
    print(f"Já consultados: {len(consultados)}")
    print(f"Novos para processar: {len(novos)}")
    
    return novos

def acessar_fluig(navegador):
    user_fluig = os.getenv("FLUIG_USER")
    password_fluig = quote_plus(os.getenv("FLUIG_PASSWORD"))

    navegador.find_element(By.ID, "username").click()
    navegador.find_element(By.ID, "username").send_keys(user_fluig)
    navegador.find_element(By.ID, "password").click()
    navegador.find_element(By.ID, "password").send_keys(password_fluig)
    navegador.find_element(By.ID, "submitLogin").click()
    # Fechar modal se aparecer
    try:
        wait = WebDriverWait(navegador, 5)
        close_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#fluig-modal .modal-header .close")))
        close_button.click()
    except:
        pass  # Modal não apareceu, continua normalmente
    
    


def main(navegador, desligados):
    for nome in desligados:
        navegador.find_element(By.ID, "wcm-datatable-textSearch-wcmid4").click()
        navegador.find_element(By.ID, "wcm-datatable-textSearch-wcmid4").send_keys(Keys.CONTROL + "a")
        navegador.find_element(By.ID, "wcm-datatable-textSearch-wcmid4").send_keys(nome)
        time.sleep(1)  # Aguarda carregar resultados
        
        try:
            linhas = navegador.find_elements(By.CSS_SELECTOR, "#wcmid4 tbody tr:not(.jqgfirstrow)")
            
            # print na tela se o nome tiver mais de dois resultados para ajudar a identificar
            # if len(linhas) > 1:
            #     print(f"{nome} - {len(linhas)} resultados encontrados")
            
            linhas_com_erro = set()  # Rastreia índices das linhas que deram erro
    
            while True:
                # Recarrega a lista de linhas a cada iteração
                linhas = navegador.find_elements(By.CSS_SELECTOR, "#wcmid4 tbody tr:not(.jqgfirstrow)")
                usuario_ativo_encontrado = False
                processou_com_sucesso = False  # Flag para saber se bloqueou algum
                
                for idx, linha in enumerate(linhas):
                    # Pula linhas que já deram erro anteriormente
                    if idx in linhas_com_erro:
                        continue
                    
                    # Verifica o status do usuário
                    status = linha.find_element(By.CSS_SELECTOR, "td[aria-describedby='wcmid4_state']").text
                    
                    if status == "ATIVO":
                        usuario_ativo_encontrado = True
                        
                        # Clica no checkbox do usuário
                        checkbox = linha.find_element(By.CSS_SELECTOR, "input[type='checkbox']")
                        checkbox.click()
                        time.sleep(0.5)
                        
                        navegador.find_element(By.CSS_SELECTOR, "a.datatable-buttonsEventFunction-wcmid4[data-key='2']").click()
                        
                        # Aguarda o modal de confirmação aparecer
                        wait = WebDriverWait(navegador, 5)
                        confirmar_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.wcm-panel-bt-custom")))
                        confirmar_btn.click()
                        
                        time.sleep(1)  # Aguarda processar o bloqueio
                        
                        # Verifica se apareceu modal de erro
                        try:
                            erro_modal = navegador.find_element(By.CSS_SELECTOR, ".wcm-panel-title")
                            if "Erro" in erro_modal.text:
                                # Fecha o modal de erro
                                navegador.find_element(By.CSS_SELECTOR, "button.wcm-panel-bt-close").click()
                                time.sleep(0.5)
                                # Desmarca o checkbox (recarrega para evitar stale element)
                                linhas_atualizadas = navegador.find_elements(By.CSS_SELECTOR, "#wcmid4 tbody tr:not(.jqgfirstrow)")
                                for linha_nova in linhas_atualizadas:
                                    try:
                                        cb = linha_nova.find_element(By.CSS_SELECTOR, "input[type='checkbox']")
                                        if cb.is_selected():
                                            cb.click()
                                            break
                                    except:
                                        pass
                                # Adiciona o índice ao set de erros
                                linhas_com_erro.add(idx)
                                # CONTINUA o for para tentar a próxima linha
                                continue
                        except:
                            pass  # Não há modal de erro, bloqueio foi bem-sucedido
                        
                        # Se chegou aqui, foi SUCESSO - ajusta os índices do set de erros
                        linhas_com_erro = {i - 1 if i > idx else i for i in linhas_com_erro}
                        processou_com_sucesso = True
                        break  # Sai do for para recarregar a lista no while
                
                # Sai do while se não tem mais ativos OU se percorreu todos sem conseguir bloquear nenhum
                if not usuario_ativo_encontrado or (usuario_ativo_encontrado and not processou_com_sucesso):
                    break

        except Exception as e:
            print(f"Erro ao processar {nome}: {str(e)}")
        
        # Salva o nome como consultado SEMPRE, independente do resultado
        salvar_consultado(nome)

# Função que será executada por cada processo (FORA do if __name__)
def processar_navegador(nomes):
    navegador = iniciar_navegador()
    acessar_fluig(navegador)
    main(navegador, nomes)
    navegador.quit()

if __name__ == "__main__":
    # Busca todos os desligados
    todos_desligados = buscar_desligados()
    # Filtra apenas os novos que ainda não foram consultados
    desligados = filtrar_novos_desligados(todos_desligados)
    # desligados = ["LUCIANA FREITAS GUEDES", "EVERARDO DE SOUSA MACIEL", "MARIA TATIANE FERREIRA LIMA", "EVALDO SOUSA MESQUITA"]
    if len(desligados) == 0:
        print("Nenhum novo funcionário para processar!")
    else:
        QUANTIDADE_NAVEGADORES = 9
        
        # Divide a lista em partes aproximadamente iguais
        k, m = divmod(len(desligados), QUANTIDADE_NAVEGADORES)
        lista_nomes = [desligados[i*k + min(i, m):(i+1)*k + min(i+1, m)] for i in range(QUANTIDADE_NAVEGADORES)]
        
        #prints de quantidade de cada navegador para processar nomes:
        for i, nomes in enumerate(lista_nomes):
            print(f"Navegador {i+1} processará {len(nomes)} nomes")
        
        # Cria e inicia os processos
        processos = []
        for nomes in lista_nomes:
            if len(nomes) > 0:  # Só cria processo se houver nomes para processar
                p = Process(target=processar_navegador, args=(nomes,))
                p.start()
                processos.append(p)
                time.sleep(2)  # Delay entre abrir cada navegador
        
        # Aguarda todos os processos terminarem
        for p in processos:
            p.join()
        
        print("Processamento concluído!")
