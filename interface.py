from monitoramento_de_preco import projeto_monitorar_preco
import PySimpleGUI as sg
from threading import Thread
import schedule
from time import sleep

def executar_schedule(intervalo, window, site):
    schedule.every(intervalo).minutes.do(projeto_monitorar_preco, window, site)
    while True:
        schedule.run_pending()
        sleep(1)
sg.theme('black')

layout = [
    [sg.Text('digite o URL de um produto do site da Kabum',size=(20,1))],
    [sg.Input(key='site')],
    [sg.Text('a cada quantos minutos você deseja verificar o site')],
    [sg.Input(key='tempo')],
    [sg.Text('Iniciar a primeira vez imediatamente?'), sg.Checkbox('Sim',key='iniciar_imediatamente')],
    [sg.Button('Buscar', key='buscar'), sg.Button('Encerrar programa', key='encerrar',  button_color='RED')],
    [sg.Output(size=(45,10))],
]

window = sg.Window('busca de preço', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

    elif event == 'buscar':
        site = values['site']
        try:
            intervalo = float(values['tempo'])
        except:
            print("pro favor, digite apenas numeros")
            continue

        running = True
        if values['iniciar_imediatamente'] == True:
            thread_bot = Thread(target=projeto_monitorar_preco,args=(window, site), daemon=True)
            thread_bot.start()
        print(f'programa iniciando em {values["tempo"]} minutos, por favor aguarde')
        thread_bot = Thread(target=executar_schedule,args=(intervalo, window, site), daemon=True)
        thread_bot.start()
        window['buscar'].update(disabled=True)

    elif event == 'planilha_atualizada':
        # thread_bot.join()
        print(values['planilha_atualizada'])
        window['buscar'].update(disabled=False)
        print(f'próxima atualização em {values["tempo"]} minutos')

    elif event == 'encerrar':
        break