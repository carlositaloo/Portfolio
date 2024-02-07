# pyinstaller --onefile --noconsole --icon=icon.ico --add-data "icon.png;." main_installer.py

from os import _exit
from subprocess import Popen
from pynput.keyboard import Key, Listener
from PIL import Image
from time import time, sleep
from pygetwindow import getActiveWindow
from keyboard import send
import pystray

# Códigos de teclas
tecla_calculadora = Key.num_lock
tecla_notepad = 111  # Código da tecla 'notepad'
tecla_ponto = 161  # Código da tecla '.'

# Configurações
limite_pressionamentos = 2
intervalo_pressionamento = 0.5

# Variáveis globais
pressionamentos = 0
ultimo_tempo = 0
app_aberto = False
tecla_pressionada = False

# Função para abrir um aplicativo
def abrir_aplicativo(nome_aplicativo, pressionamentos, app_aberto):
    if pressionamentos >= limite_pressionamentos and not app_aberto:
        Popen([nome_aplicativo])
        sleep(2)
        return True
    return False

# Função de callback para quando uma tecla é pressionada
def ao_pressionar(key):
    global pressionamentos, ultimo_tempo, tecla_pressionada, app_aberto

    try:
        codigo_tecla_press = key.vk
    except AttributeError:
        codigo_tecla_press = key.value.vk

    if not tecla_pressionada:
        tecla_pressionada = True
        tempo_atual = time()

        if tempo_atual - ultimo_tempo <= intervalo_pressionamento:
            pressionamentos += 1
        else:
            pressionamentos = 1

        ultimo_tempo = tempo_atual

        if key == tecla_calculadora:
            app_aberto = abrir_aplicativo("calc.exe", pressionamentos, app_aberto)
        elif codigo_tecla_press == tecla_notepad:
            app_aberto = abrir_aplicativo("notepad.exe", pressionamentos, app_aberto)
            
    if codigo_tecla_press == tecla_ponto:
        if getActiveWindow().title == "Calculadora":
            send('shift+5')

# Função de callback para quando uma tecla é solta
def ao_soltar(key):
    global tecla_pressionada, app_aberto
    tecla_pressionada = False
    app_aberto = False

# Função para sair do programa
def sair_do_programa(icon, item):
    icon.stop()
    _exit(0)

# Carregamento do ícone
img_icon = Image.open("icon.png")

# Configuração do ícone na bandeja do sistema
icon = pystray.Icon("Copy nota", img_icon, menu=pystray.Menu(
    pystray.MenuItem("Quit", sair_do_programa)
))

# Iniciar o Listener
with Listener(on_press=ao_pressionar, on_release=ao_soltar) as listener:
    icon.run()
    listener.join()
