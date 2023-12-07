from pynput.keyboard import Key, Listener
import time
import subprocess
import os

# Configurações
limite_pressionamentos = 2  # Número de vezes que a tecla deve ser pressionada
intervalo_pressionamento = 0.5  # Intervalo de tempo para considerar pressionamentos sucessivos (em segundos)

# Variáveis globais
pressionamentos = 0
ultimo_tempo = 0
app_aberto = False
tecla_pressionada = False

def ao_pressionar(key):
    global pressionamentos, ultimo_tempo, tecla_pressionada

    try:
        codigo_tecla_press = key.vk
    except AttributeError:
        codigo_tecla_press = key.value.vk

    if not tecla_pressionada:
        tecla_pressionada = True
        tempo_atual = time.time()

        if tempo_atual - ultimo_tempo <= intervalo_pressionamento:
            pressionamentos += 1
        else:
            pressionamentos = 1

        ultimo_tempo = tempo_atual

        if key == Key.num_lock:
            abrir_calculadora()
        elif codigo_tecla_press == 111:  # Comparação com o código da tecla
            abrir_notepad()


def abrir_calculadora():
    global pressionamentos, app_aberto
    if pressionamentos >= limite_pressionamentos and not app_aberto:
        subprocess.Popen(["calc.exe"])
        app_aberto = True
        # print("Calculadora aberta!")

def abrir_notepad():
    global pressionamentos, app_aberto
    if pressionamentos >= limite_pressionamentos and not app_aberto:
        subprocess.Popen(["notepad.exe"])
        app_aberto = True
        # print("Bloco de notas aberto!")

def ao_soltar(key):
    global tecla_pressionada, app_aberto
    tecla_pressionada = False
    app_aberto = False

# Limpar a tela no início
os.system("cls" if os.name == 'nt' else 'clear')

# Iniciar o Listener
with Listener(on_press=ao_pressionar, on_release=ao_soltar) as listener:
    listener.join()
