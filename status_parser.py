import requests
from bs4 import BeautifulSoup
import feedparser
from datetime import datetime
import re


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
    return "All services are operating normally"  # if all services are operating normally


def cloudflare():
    link = "https://www.cloudflarestatus.com/history.atom"
    feed = feedparser.parse(link)
    issues = []
    date = datetime.utcnow().strftime('%Y-%m-%d')  # cloudflare uses UTC
    for entry in feed["entries"]:
        if date in entry["updated"]:  # filter out entries that are not from today
            issues.append(entry["title"])
            issues.append(entry["link"])
    if issues != []:
        return str(issues)
    else:
        return "All systems operational"


def google_cloud():
    link = "https://status.cloud.google.com/en/feed.atom"  # no date filtering needed, they only return current status
    feed = feedparser.parse(link)
    issues = []
    for entry in feed["entries"]:
        issues.append(entry["title"])
        issues.append(entry["link"])
    if issues != []:
        return str(issues)
    else:
        return "All systems operational"


def voipms():
    link = "https://status.voip.ms/history.rss"
    feed = feedparser.parse(link)
    issues = []
    date = datetime.utcnow().strftime('%Y-%m-%d')  # voip.ms uses UTC
    for entry in feed["entries"]:
        if date in entry["updated"]:  # filter out entries that are not from today
            issues.append(entry["title"])
            issues.append(entry["link"])
    if issues != []:
        return str(issues)
    else:
        return "All systems operational"


def freshservice():
    link = "https://updates.freshservice.com/"
    html = requests.get(link).text
    soup = BeautifulSoup(html, "html.parser")
    print(soup.prettify())

    status = soup.findAll("script", {'id': '__NEXT_DATA__'})
    print(status)
    if status.text != "All Services Operational":
        return status.text
    else:
        return "All systems operational"


print("### AWS STATUS ### \n" + aws() + "\n")
print("### CLOUDFLARE STATUS ### \n" + cloudflare() + "\n")
print("### GOOGLE CLOUD STATUS ### \n" + google_cloud() + "\n")
print("### VOIP.MS STATUS ### \n" + voipms() + "\n")
print("### FRESHSERVICE STATUS ### \n" + freshservice() + "\n")
