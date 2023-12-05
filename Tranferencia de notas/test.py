from pynput.keyboard import Key, Listener
import time
import subprocess
import os

os.system("cls")

tecla = Key.num_lock # Defina a tecla que você quer usar para abrir a calculadora

tecla_pressionada = False
tempo_tecla_pressionada = 0
calculadora_aberta = False  # Adicione esta variável de controle

def ao_pressionar(key):
    # print(key)
    global tecla_pressionada, tempo_tecla_pressionada, calculadora_aberta
    if key == tecla:
        if not tecla_pressionada:
            tecla_pressionada = True
            tempo_tecla_pressionada = time.time()
            print("Tecla pressionada!")
        else:
            if not calculadora_aberta and time.time() - tempo_tecla_pressionada >= 1:
                subprocess.Popen(["calc.exe"])
                calculadora_aberta = True  # Defina a calculadora como aberta
                print("Calculadora aberta!")
    else:
        tecla_pressionada = False

def ao_soltar(key):
    global tecla_pressionada, calculadora_aberta
    if key == tecla:
        tecla_pressionada = False
        calculadora_aberta = False
        print("Tecla solta!")

# Iniciar o listener
with Listener(on_press=ao_pressionar, on_release=ao_soltar) as listener:
    listener.join()
