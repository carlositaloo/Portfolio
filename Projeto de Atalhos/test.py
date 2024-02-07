from pynput.keyboard import Listener


def ao_pressionar(key):
    try:
        print('Tecla pressionada: {0}, com código: {1}'.format(key, key.vk))
    except AttributeError:
        print('Tecla especial pressionada: {0}, com código: {1}'.format(
            key, key.value.vk))


# Iniciar o Listener
with Listener(on_press=ao_pressionar) as listener:
    listener.join()
