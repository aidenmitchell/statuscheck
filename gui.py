import status_parser
import internet_check
import PySimpleGUI as Gui
import time

aws = status_parser.aws()
cloudflare = status_parser.cloudflare()
google_cloud = status_parser.google_cloud()
freshservice = status_parser.freshservice()
voipms = status_parser.generic_rss("https://status.voip.ms/history.rss", "voip.ms")
ping_hosts = ['1.1.1.1', '8.8.8.8', 'dc01', 'dc02']
ping = internet_check.multi_ping(ping_hosts)

statuses = [aws, cloudflare, google_cloud, freshservice, voipms]
for status in statuses:
    if "All systems operational" not in status:
        title = "Incident - " + status
        bg_color = 'red'
    elif any('0' in x for x in ping):
        title = "Unable to reach host"
        bg_color = 'orange'
    else:
        title = "All systems operational"
        bg_color = 'green'


def refresh():
    aws = status_parser.aws()
    cloudflare = status_parser.cloudflare()
    google_cloud = status_parser.google_cloud()
    freshservice = status_parser.freshservice()
    voipms = status_parser.generic_rss("https://status.voip.ms/history.rss", "voip.ms")
    ping = internet_check.multi_ping(ping_hosts)

    statuses = [aws, cloudflare, google_cloud, freshservice, voipms]
    for status in statuses:
        if "All systems operational" not in status:
            title = "Incident - " + status
            bg_color = 'red'
        elif any('0' in x for x in ping):
            title = "Unable to reach host"
            bg_color = 'orange'
        else:
            title = "All systems operational"
            bg_color = 'green'
    window['refresh'].update(title, background_color=bg_color)
    window['refresh0'].update(aws)
    window['refresh1'].update(cloudflare)
    window['refresh2'].update(google_cloud)
    window['refresh3'].update(freshservice)
    window['refresh4'].update(voipms)
    window['refresh5'].update(values=ping)

# sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
layout = [[Gui.Text(title, key='refresh', background_color=bg_color)],
          [Gui.Text(aws, key='refresh0')],
          [Gui.Text(cloudflare, key='refresh1')],
          [Gui.Text(google_cloud, key='refresh2')],
          [Gui.Text(freshservice, key='refresh3')],
          [Gui.Text(voipms, key='refresh4')],
          [Gui.Table(values=ping, headings=["Host", "Ping (ms)"], auto_size_columns=True, hide_vertical_scroll=True, key='refresh5')],
          [Gui.Button('Refresh')], [Gui.Text("", key='done')]]

# Create the Window
window = Gui.Window('Statuses', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == 'Refresh':
        window.perform_long_operation(refresh, 'done')
    elif event == 'done':
        window['done'].update('Refreshed at ' + time.strftime("%H:%M:%S"))
    elif event == Gui.WIN_CLOSED:  # if user closes window or clicks cancel
        break

window.close()
