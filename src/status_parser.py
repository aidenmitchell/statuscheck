import requests
from bs4 import BeautifulSoup
import feedparser
from datetime import datetime
import json
import re


def aws():
    try:
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
                return ("AWS: Issue in " + region + ": " + statuses[regions.index(region)].text + "\nIssue: " + messages[
                    0].text)  # return the first issue
        return "AWS: All systems operational"  + "\n" + reddit_search(keywords) # if all services are operating normally
    except requests.exceptions.ConnectionError:
        return "AWS: Unable to connect to AWS status page"



def generic_rss(link, service_name, keywords):
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
        return service_name + str(issues)
    else:
        return service_name + ": All systems operational" + "\n" + reddit_search(keywords)


def statuspage(link, service_name, keywords):  # for any pages using Atlassian Statuspage
    page = link
    html = requests.get(page).text
    soup = BeautifulSoup(html, "html.parser")
    status = soup.find("a", {'class': 'actual-title'})  # get banner text
    if status is None:
        return service_name + ": All systems operational" + "\n" + reddit_search(keywords)
    elif "All Services Operational" not in status.text:
        return service_name + ": " + str(status.text)


def microsoft():
    feed = feedparser.parse("https://nitter.net/MSFT365Status/rss")
    keywords = ["microsoft", "microsoft 365", "o365", "office 365", "microsoft online", "ms"]
    try:
        if "mitigated" in feed["entries"][0]["title"] or "resolved" in feed["entries"][0]["title"]:
            return "Microsoft 365: All systems operational" + "\n" + reddit_search(keywords)
        else:
            return "Microsoft 365: " + str(feed["entries"][0]["title"])
    except IndexError:
        return "Microsoft 365: All systems operational" + "\n" + reddit_search(keywords)


def google_cloud():
    # combines status from their rss feed and their website
    # because Google doesn't publish all incidents in their rss feed :(
    link = "https://status.cloud.google.com/"
    html = requests.get(link).text
    soup = BeautifulSoup(html, "html.parser")

    keywords = ["google cloud", "google cloud platform", "google cloud services"]
    messages = soup.find("div", {'class': 'banner'})  # get banner text
    feed = feedparser.parse("https://status.cloud.google.com/en/feed.atom")
    issues = []
    date = datetime.utcnow().strftime('%Y-%m-%d')  # most rss feeds use UTC
    for entry in feed["entries"]:
        if date in entry["updated"] and "RESOLVED" not in entry["title"]:  # filter out entries that are not from today
            issues.append(entry["title"])
            issues.append(entry["link"])
    if issues:  # return rss incidents first
        return "Google Cloud: " + str(issues[0])
    elif messages:  # return page banner if no rss incidents
        return "Google Cloud: " + str(messages.text)
    else:  # return "All systems operational" if no incidents
        return "Google Cloud: All systems operational" + "\n" + reddit_search(keywords)


def freshservice():
    # freshservice doesn't have a rss feed, so they get their own function
    link = "https://updates.freshservice.com/"
    html = requests.get(link).text
    soup = BeautifulSoup(html, "html.parser")
    keywords = ["freshservice", "freshservice status", "freshstatus"]

    web_json = soup.find("script", {'id': '__NEXT_DATA__'}).string  # get json data from the page
    status = json.loads(web_json)["props"]["pageProps"]["accountDetails"]["branding_data"]["topBandText"]  # get status
    if "All Services Operational" not in status:
        return "Freshservice: " + str(status)
    else:
        return "Freshservice: All systems operational" + "\n" + reddit_search(keywords)


def reddit_search(keywords):
    rss_feed = "https://www.reddit.com/r/sysadmin/new.rss"
    feed = feedparser.parse(rss_feed)
    posts = []
    for entry in feed["entries"]:
        # print(entry["content"][0]["value"])
        for keyword in keywords:
            if re.search(keyword, entry["content"][0]["value"]) or re.search(keyword, entry["title"]):  # regex to filter out non-whole keywords
                posts.append(entry["title"] + ": " + entry["link"])
                # print(keyword + entry["title"] + ": " + entry["link"])
    return str(len(posts)) + " mentions on r/sysadmin"


def outage_search(keywords):
    rss_feed = "https://www.reddit.com/r/sysadmin/new.rss"
    feed = feedparser.parse(rss_feed)
    posts = []
    for entry in feed["entries"]:
        for keyword in keywords:
            if re.search(keyword, entry["title"]):  # regex to filter out non-whole keywords
                posts.append([entry["title"], entry["link"]])
    return posts  # return list of titles and links
