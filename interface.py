from monitoramento_de_preco import projeto_monitorar_preco
import PySimpleGUI as sg
from threading import Thread
import schedule
from time import sleep


running = False

def executar_schedule(intervalo, window, site):
    global running
    schedule.every(intervalo).minutes.do(projeto_monitorar_preco, window, site)
    while running:
        schedule.run_pending()
        sleep(1)
    print("Agendamento de tarefas parado.")

sg.theme('Black')

layout = [
    [sg.Text('Digite o URL de um produto do site da Kabum', size=(40,1))],
    [sg.Input(key='site')],
    [sg.Text('A cada quantos minutos você deseja verificar o site')],
    [sg.Input(key='tempo')],
    [sg.Text('Iniciar a primeira vez imediatamente?'), sg.Checkbox('Sim', key='iniciar_imediatamente')],
    [sg.Button('Buscar', key='buscar'), sg.Button('Parar Automação', key='parar', button_color='YELLOW')],
    [sg.Button('Encerrar Programa', key='encerrar', button_color='RED')],
    [sg.Output(size=(45,10))],
]

window = sg.Window('Busca de Preço', layout)


thread_bot = None

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'encerrar':
        running = False
        break

    elif event == 'buscar':
        site = values['site']
        try:
            intervalo = int(values['tempo'])
        except ValueError:
            print("Por favor, digite apenas números inteiros.")
            continue

        running = True
        if values['iniciar_imediatamente']:
            thread_inicial = Thread(target=projeto_monitorar_preco, args=(window, site), daemon=True)
            thread_inicial.start()
        
        print(f'Programa iniciando em {intervalo} minutos, por favor aguarde.')
        thread_bot = Thread(target=executar_schedule, args=(intervalo, window, site), daemon=True)
        thread_bot.start()
        window['buscar'].update(disabled=True)
        window['parar'].update(disabled=False)

    elif event == 'parar':
        running = False
        if thread_bot is not None:
            thread_bot.join()
        window['buscar'].update(disabled=False)
        print("Automação parada.")

    elif event == 'iniciando_automacao':
        window['parar'].update(disabled=True)

    elif event == 'planilha_atualizada':
        window['parar'].update(disabled=False)
        print(values['planilha_atualizada'])
        print(f'Próxima atualização em {values["tempo"]} minutos')

window.close()
