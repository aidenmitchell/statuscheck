import status_parser
import internet_check
import PySimpleGUI as Gui
import time
import webbrowser

font_size = ('Arial', 12)

def get_info():
    global aws, cloudflare, google_cloud, microsoft, freshservice, voipms, ping, statuses, title, bg_color, outage_mentions, outages, reddit
    aws = status_parser.aws()
    cloudflare = status_parser.statuspage("https://cloudflarestatus.com", "Cloudflare", ["Cloudflare"])
    google_cloud = status_parser.google_cloud()
    microsoft = status_parser.microsoft()
    freshservice = status_parser.freshservice()
    voipms = status_parser.generic_rss("https://status.voip.ms/history.rss", "voip.ms", ["voip.ms"])
    reddit = status_parser.statuspage("https://redditstatus.com", "Reddit", ["Reddit"])
    outages = status_parser.outage_search(["outage", "down"])
    outage_mentions = len(status_parser.outage_search(["outage", "down"]))  # outage keywords
    ping_hosts = ['8.8.8.8']  # ping hosts
    ping = internet_check.multi_ping(ping_hosts)

    statuses = [aws, cloudflare, google_cloud, freshservice, voipms]
    for status in statuses:
        if "All systems operational" not in status:  # if a service reports a non-operational status
            title = "Incident - " + status
            bg_color = 'red'
            break
        elif any('0' in x for x in ping):  # if a host does not respond to ping
            title = "Unable to reach host"
            bg_color = 'orange'
            break
        elif outage_mentions > 2:  # if more than 2 outage keywords are mentioned on r/sysadmin
            title = "Possible outage"
            bg_color = 'orange'
            break
        else:
            title = "All systems operational"
            bg_color = 'green'


def refresh():
    get_info()  # re-run the functions to get the new info
    # refresh the window and fields
    window['refresh'].update(title, background_color=bg_color)
    window['refresh0'].update(aws)
    window['refresh1'].update(cloudflare)
    window['refresh2'].update(google_cloud)
    window['refresh8'].update(microsoft)
    window['refresh3'].update(freshservice)
    window['refresh4'].update(voipms)
    window['refresh9'].update(reddit)
    window['refresh6'].update(str(outage_mentions) + " mentions of outages on r/sysadmin")
    window['refresh5'].update(ping)
    window['refresh7'].update(outages)


def refresh_constant():
    while True:  # refresh every 60 seconds
        refresh()
        window['done'].update('Refreshed at ' + time.strftime("%r"))  # update the refresh time
        time.sleep(30)


# sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
get_info()
layout = [[Gui.Text(title, font=font_size, key='refresh', background_color=bg_color)],
          [Gui.Text(aws, font=font_size, key='refresh0')],
          [Gui.Text(cloudflare, font=font_size, key='refresh1')],
          [Gui.Text(google_cloud, font=font_size, key='refresh2')],
          [Gui.Text(microsoft, font=font_size, key='refresh8')],
          [Gui.Text(freshservice, font=font_size, key='refresh3')],
          [Gui.Text(voipms, font=font_size, key='refresh4')],
          [Gui.Text(reddit, font=font_size, key='refresh9')],
          [Gui.Table(ping, font=font_size, headings=["Host", "Ping (ms)"], auto_size_columns=True, hide_vertical_scroll=True, num_rows=4, key='refresh5')],  # ping table
          [Gui.Text(str(outage_mentions) + " mentions of outages on r/sysadmin", font=font_size, key='refresh6')],  # outage mentions
          [Gui.Table(outages, headings=["Title", "Link (click to open)"], font=font_size, hide_vertical_scroll=True, enable_click_events=True, auto_size_columns=True, max_col_width=35, key='refresh7')],  # outages table
          [Gui.Button('Refresh', font=font_size)], [Gui.Text("", key='done', font=font_size)]]  # refresh button

# Create the Window
window = Gui.Window('Statuses', layout, keep_on_top=True, resizable=True)
# Event Loop to process "events" and get the "values" of the inputs
window.perform_long_operation(refresh_constant, 'done')  # start the 1 minute refresh
while True:
    event, values = window.read()
    if event == 'Refresh':
        window.perform_long_operation(refresh, 'done')
    elif isinstance(event, tuple):  # click on link to Reddit post
        try:  # clicking anywhere on the table can cause an error
            row, col = (event[2])  # get coordinates of the clicked cell
            link = (outages[row][col])  # get text from that coordinate
            if col == 1:  # only try to open text from the links column
                webbrowser.open(link)
        except:
            pass
    elif event == 'done':
        window['done'].update('Refreshed at ' + time.strftime("%r"))
    elif event == Gui.WIN_CLOSED:  # if user closes window or clicks cancel
        break

window.close()
