import PySimpleGUI as sg

# Crie uma lista de tarefas inicialmente vazia
tarefas = []

# Defina o layout da janela
layout = [
    [sg.InputText(key='-TAREFA-', size=(30, 1)), sg.Button('Adicionar')],
    [sg.Listbox(values=tarefas, size=(30, 10), key='-LISTA-')],
]

# Crie a janela
window = sg.Window('Lista de Tarefas', layout)

# Loop principal da aplicação
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break

    if event == 'Adicionar':
        tarefa = values['-TAREFA-']
        if tarefa:
            tarefas.append(tarefa)
            window['-LISTA-'].update(values=tarefas)
            window['-TAREFA-'].update('')

    if event == '-LISTA-':
        # Marque ou desmarque a tarefa ao clicar nela na lista
        index = values['-LISTA-'][0]
        if index < len(tarefas):
            tarefa = tarefas[index]
            tarefas[index] = f'✔ {tarefa}' if not tarefa.startswith('✔') else tarefa.lstrip('✔ ')
            window['-LISTA-'].update(values=tarefas)

window.close()
