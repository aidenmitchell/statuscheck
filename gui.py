import status_parser
import internet_check
import PySimpleGUI as Gui

status = status_parser.all_statuses()
if "Incident" in status:
    bg_color = 'red'
else:
    bg_color = 'green'


def refresh():
    window['refresh'].update(status_parser.all_statuses(), background_color=bg_color)
    window['refresh0'].update(status_parser.aws())
    window['refresh1'].update(status_parser.google_cloud())
    window['refresh2'].update(status_parser.freshservice())
    window['refresh3'].update(status_parser.generic_rss("https://status.voip.ms/history.rss", "voip.ms"))
    window['refresh4'].update("Ping: " + internet_check.multi_ping(['1.1.1.1', '8.8.8.8']))


# sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
layout = [[Gui.Text(status_parser.all_statuses(), key='refresh', background_color=bg_color)],
          [Gui.Text(status_parser.aws(), key='refresh0')],
          [Gui.Text(status_parser.google_cloud(), key='refresh1')],
          [Gui.Text(status_parser.freshservice(), key='refresh2')],
          [Gui.Text(status_parser.generic_rss("https://status.voip.ms/history.rss", "voip.ms"), key='refresh3')],
          [Gui.Text("Ping: " + internet_check.multi_ping(['1.1.1.1', '8.8.8.8']), key='refresh4')],
          [Gui.Button('Refresh')]]

# Create the Window
window = Gui.Window('Statuses', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == 'Refresh':
        refresh()
    elif event == Gui.WIN_CLOSED:  # if user closes window or clicks cancel
        break

window.close()
