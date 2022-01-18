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
        if statuses[regions.index(region)].text != "All services are operating normally":
            return ("Issue in " + region + ": " + statuses[regions.index(region)].text + "\nIssue: " + messages[
                0].text)
    return "All services are operating normally"


def cloudflare():
    link = "https://www.cloudflarestatus.com/history.atom"
    feed = feedparser.parse(link)
    issues = []
    date = datetime.utcnow().strftime('%Y-%m-%d')  # cloudflare uses UTC
    for entry in feed["entries"]:
        if date in entry["updated"]:
            issues.append(entry["title"])
            issues.append(entry["link"])
    return str(issues)


def google_cloud():
    link = "https://status.cloud.google.com/en/feed.atom"
    feed = feedparser.parse(link)
    issues = []
    for entry in feed["entries"]:
        issues.append(entry["title"])
        issues.append(entry["link"])
    return str(issues)


print("### AWS STATUS ### \n" + aws() + "\n")
print("### CLOUDFLARE STATUS ### \n" + cloudflare() + "\n")
print("### GOOGLE CLOUD STATUS ### \n" + google_cloud())
