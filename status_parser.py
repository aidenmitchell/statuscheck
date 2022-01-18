import requests
from bs4 import BeautifulSoup
import feedparser
from datetime import datetime
import json


def aws():
    link = "https://aws-status.info/"
    html = requests.get(link).text
    soup = BeautifulSoup(html, "html.parser")

    regions = ["North America", "South America", "Europe", "Asia Pacific"]
    statuses = soup.findAll("span", {'class': 'label'})
    messages = soup.findAll("span", {'class': 'message'})

    for region in regions:
        if statuses[regions.index(region)].text != "All services are operating normally":  # if any service is not
            # operating normally
            return ("Issue in " + region + ": " + statuses[regions.index(region)].text + "\nIssue: " + messages[
                0].text)  # return the first issue
    return "All systems operational"  # if all services are operating normally


def generic_rss(link):
    feed = feedparser.parse(link)
    issues = []
    date = datetime.utcnow().strftime('%Y-%m-%d')  # most rss feeds use UTC
    for entry in feed["entries"]:
        if date in entry["updated"]:  # filter out entries that are not from today
            issues.append(entry["title"])
            issues.append(entry["link"])
    if issues:
        return str(issues)
    else:
        return "All systems operational"


def google_cloud():
    link = "https://status.cloud.google.com/"
    html = requests.get(link).text
    soup = BeautifulSoup(html, "html.parser")

    messages = soup.find("div", {'class': 'banner'})
    feed = feedparser.parse("https://status.cloud.google.com/en/feed.atom")
    issues = []
    date = datetime.utcnow().strftime('%Y-%m-%d')  # most rss feeds use UTC
    for entry in feed["entries"]:
        if date in entry["updated"]:  # filter out entries that are not from today
            issues.append(entry["title"])
            issues.append(entry["link"])
    if issues:
        return str(issues)
    elif messages:
        return str(messages.text)
    else:
        return "All systems operational"


def cloudflare():
    feed = feedparser.parse("https://www.cloudflarestatus.com/history.atom")
    issues = []
    date = datetime.utcnow().strftime('%Y-%m-%d')  # most rss feeds use UTC
    for entry in feed["entries"]:
        if "resolved" in entry["content"][0]["value"]:  # if the latest entry is resolved
            return "All systems operational"
        elif date in entry["updated"]:  # ensure that the entry is from today
            issues.append(entry["title"])
            issues.append(entry["link"])
    return str(issues)


def freshservice():
    link = "https://updates.freshservice.com/"
    html = requests.get(link).text
    soup = BeautifulSoup(html, "html.parser")

    web_json = soup.find("script", {'id': '__NEXT_DATA__'}).string  # get json data from the page
    status = json.loads(web_json)["props"]["pageProps"]["accountDetails"]["branding_data"]["topBandText"]  # get status
    if "All Services Operational" not in status:
        return str(status)
    else:
        return "All systems operational"


print("### AWS STATUS ### \n" + aws() + "\n")
print("### CLOUDFLARE STATUS ### \n" + cloudflare() + "\n")
print("### GOOGLE CLOUD STATUS ### \n" + google_cloud() + "\n")
print("### VOIP.MS STATUS ### \n" + generic_rss("https://status.voip.ms/history.rss") + "\n")
print("### FRESHSERVICE STATUS ### \n" + freshservice() + "\n")
