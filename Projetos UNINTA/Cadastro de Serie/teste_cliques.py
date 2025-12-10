import pyautogui
import time
import keyboard  # Importa a biblioteca keyboard

# Configurações iniciais
inicio_x = 1057
inicio_y = 353
incremento_cord = 19
num_cliques = 15

# Tempo de espera antes de começar os cliques
time.sleep(5)  # Aguarde 5 segundos para você mudar para a janela correta

# Simulação de cliques
def simular_cliques():
    for i in range(num_cliques):
        # Verifica se a tecla ESC foi pressionada
        if keyboard.is_pressed('esc'):
            print("Script interrompido pelo usuário.")
            break  # Interrompe o loop se ESC for pressionado
        
        # Calcula a nova coordenada
        nova_y = inicio_y + (i * incremento_cord)
        # Clique na nova coordenada
        pyautogui.click(inicio_x, nova_y, duration=0.15)
        time.sleep(0.5)  # Aguarde um pouco entre os cliques

if __name__ == "__main__":
    simular_cliques()