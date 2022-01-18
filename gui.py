import status_parser
import internet_check
import PySimpleGUI as sg

def refresh():
    window['refresh'].update(internet_check.multi_ping(['1.1.1.1', '8.8.8.8']))


# sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
layout = [  [sg.Text("AWS: " + status_parser.aws(), key='refresh')],
            [sg.Text("Google Cloud: " + status_parser.google_cloud())],
            [sg.Text("Freshservice: " + status_parser.freshservice())],
            [sg.Text("Freshservice: " + internet_check.multi_ping(['1.1.1.1', '8.8.8.8']), key='refresh')],
            [sg.Button('Refresh')]]

# Create the Window
window = sg.Window('Statuses', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == 'Refresh':
        refresh()
    elif event == sg.WIN_CLOSED: # if user closes window or clicks cancel
        break

window.close()
