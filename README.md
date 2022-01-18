# statuscheck

Functions to check the various statuses of online services, will eventually include a GUI.

## status_parser.py

Pulls the system status directly from the vendor's status page.
Currently includes:
 - AWS
 - Cloudflare
 - Freshservice
 - Google Cloud
 - Any other generic RSS status feed
 
Will include:
 - Monitoring of Twitter feeds for status
 - Monitoring of subreddits for status (measure mentions of a specific service to detect downtime before it is posted on their status page)

## internet_check.py

Pings various internet services and returns their ping time.
Example output:
```
1.1.1.1 6.046 ms
8.8.8.8 9.032 ms
```
