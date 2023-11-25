from pynput.keyboard import Key, Listener
import time
import subprocess
import os

os.system("cls")

tecla = Key.num_lock
limite_pressionamentos = 2
intervalo = 0.5

pressionamentos = 0
ultimo_tempo = 0
calculadora_aberta = False
tecla_pressionada = False  # Variável para rastrear o estado da tecla

def ao_pressionar(key):
    global pressionamentos, ultimo_tempo, calculadora_aberta, tecla_pressionada

    if key == tecla and not tecla_pressionada:
        tecla_pressionada = True  # Marcar a tecla como pressionada
        tempo_atual = time.time()

        if tempo_atual - ultimo_tempo <= intervalo:
            pressionamentos += 1
        else:
            pressionamentos = 1

        ultimo_tempo = tempo_atual

        if pressionamentos >= limite_pressionamentos and not calculadora_aberta:
            subprocess.Popen(["calc.exe"])
            calculadora_aberta = True
            print("Calculadora aberta!")

def ao_soltar(key):
    global calculadora_aberta, tecla_pressionada
    if key == tecla:
        calculadora_aberta = False
        tecla_pressionada = False  # Marcar a tecla como solta
        print("Calculadora fechada.")

with Listener(on_press=ao_pressionar, on_release=ao_soltar) as listener:
    listener.join()
