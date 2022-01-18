import requests
from bs4 import BeautifulSoup
import feedparser
from datetime import datetime
import json


def aws():
    # aws has rss feeds, but only for each service, so scraping is needed to get an overview
    link = "https://aws-status.info/"  # this website is better than AWS's status page
    html = requests.get(link).text
    soup = BeautifulSoup(html, "html.parser")

    keywords = ["aws", "amazon web services"]  # for future implementation of subreddit monitoring
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
    # should be used for all rss feeds that don't have a specific function like voip.ms
    # example link: https://status.voip.ms/history.rss
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
    # combines status from their rss feed and their website
    # because Google doesn't publish all incidents in their rss feed :(
    link = "https://status.cloud.google.com/"
    html = requests.get(link).text
    soup = BeautifulSoup(html, "html.parser")

    keywords = ["google", "cloud", "google cloud", "google cloud platform", "google cloud services"]
    messages = soup.find("div", {'class': 'banner'})  # get banner text
    feed = feedparser.parse("https://status.cloud.google.com/en/feed.atom")
    issues = []
    date = datetime.utcnow().strftime('%Y-%m-%d')  # most rss feeds use UTC
    for entry in feed["entries"]:
        if date in entry["updated"]:  # filter out entries that are not from today
            issues.append(entry["title"])
            issues.append(entry["link"])
    if issues:  # return rss incidents first
        return str(issues)
    elif messages:  # return page banner if no rss incidents
        return str(messages.text)
    else:  # return "All systems operational" if no incidents
        return "All systems operational"


def cloudflare():
    # cloudflare includes resolved incidents in their rss feed, so they get their own function
    feed = feedparser.parse("https://www.cloudflarestatus.com/history.atom")
    keywords = ["cloudflare", "cloudflare status"]
    issues = []
    date = datetime.utcnow().strftime('%Y-%m-%d')  # most rss feeds use UTC
    for entry in feed["entries"]:
        if "resolved" in entry["content"][0]["value"]:  # if the latest entry is resolved, everything is fine
            return "All systems operational"
        elif date in entry["updated"]:  # ensure that the entry is from today
            issues.append(entry["title"])
            issues.append(entry["link"])
    return str(issues)


def freshservice():
    # freshservice doesn't have a rss feed, so they get their own function
    link = "https://updates.freshservice.com/"
    html = requests.get(link).text
    soup = BeautifulSoup(html, "html.parser")
    keywords = ["freshservice", "freshservice status", "freshstatus"]

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
