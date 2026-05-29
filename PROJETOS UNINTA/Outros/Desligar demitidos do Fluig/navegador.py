from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
import logging
import os
import time

def iniciar_navegador(worker_num=None, browser="chrome"):
    os.environ['WDM_LOG'] = '0'  # Desabilita logs do webdriver-manager
    
    logging.getLogger('selenium').setLevel(logging.CRITICAL)  # Define nível de log CRITICAL para Selenium (só erros críticos)
    logging.getLogger('urllib3').setLevel(logging.CRITICAL)  # Define nível de log CRITICAL para urllib3 (biblioteca HTTP)
    
    if browser.lower() == "edge":
        browser_options = EdgeOptions()  # Cria objeto de opções para configurar o Edge
    else:
        browser_options = ChromeOptions()  # Cria objeto de opções para configurar o Chrome
    
    browser_options.add_experimental_option('excludeSwitches', ['enable-logging'])  # Remove mensagens "DevTools listening on..."
    browser_options.add_argument('--log-level=3')  # Define nível de log: 0=INFO, 1=WARNING, 2=ERROR, 3=FATAL
    browser_options.add_argument('--disable-logging')  # Desabilita sistema de logging do Chrome
    browser_options.add_argument('--silent')  # Modo silencioso - suprime avisos não críticos
    browser_options.add_argument('--disable-gpu')  # Desabilita aceleração GPU (evita mensagens de gráficos)
    browser_options.add_argument('--disable-dev-shm-usage')  # Desabilita /dev/shm (evita problemas de memória)
    browser_options.add_argument('--no-sandbox')  # Desabilita sandbox (evita mensagens de segurança)
    browser_options.add_argument('--disable-extensions')  # Desabilita extensões do Chrome
    browser_options.add_argument('--disable-infobars')  # Desabilita barra de informações "Chrome is being controlled by automated test"
    browser_options.add_argument('--disable-blink-features=AutomationControlled')  # Desabilita detecção de automação
    browser_options.add_argument('--ignore-certificate-errors')  # Ignora erros de certificado SSL
    browser_options.add_argument('--ignore-ssl-errors')  # Ignora erros SSL
    browser_options.page_load_strategy = 'normal'  # ou 'eager' para carregar mais rápido
    
    if browser.lower() == "edge":
        service = EdgeService(log_path='NUL')  # Redireciona logs do EdgeDriver para NUL (Windows) ou /dev/null (Linux/Mac)
        navegador = webdriver.Edge(service=service, options=browser_options)  # Cria instância do Edge com configurações
    else:
        service = ChromeService(log_path='NUL')  # Redireciona logs do ChromeDriver para NUL (Windows) ou /dev/null (Linux/Mac)
        navegador = webdriver.Chrome(service=service, options=browser_options)  # Cria instância do Chrome com configurações
    
    navegador.maximize_window()  # Maximiza a janela do navegador
    navegador.get("https://fluig.aiamis.com.br/portal/p/01/wcmuserpage")  # Acessa a URL do sistema FIES

    # Aguarda um pouco para a página carregar
    time.sleep(3)
    return navegador  # Retorna o objeto navegador