#!/usr/bin/env python
# Credit to: https://www.scrapingdog.com/blog/scrape-linkedin-jobs/

import requests
from bs4 import BeautifulSoup
import math
import pandas as pd

# enter your search parameters here
target = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=cyber&location=United%20States&geoId=103644278&start={}"
o = {}
k = []
l = []

# change ceil(???/25) to the number of job listings
for i in range(0, math.ceil(8000 / 25)):
    res = requests.get(target.format(i))
    soup = BeautifulSoup(res.text, "html.parser")
    jobs_on_page = soup.find_all("li")

    for x in range(0, len(jobs_on_page)):
        jobid = (
            jobs_on_page[x]
            .find("div", {"class": "base-card"})
            .get("data-entity-urn")
            .split(":")[3]
        )
        l.append(jobid)

print("Finished gathering job IDs, now requesting job postings...")

target = "https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{}"
for j in range(0, len(l)):

    resp = requests.get(target.format(l[j]))
    soup = BeautifulSoup(resp.text, "html.parser")

    try:
        o["company"] = (
            soup.find("div", {"class": "top-card-layout__card"})
            .find("a")
            .find("img")
            .get("alt")
        )
    except:
        o["company"] = None

    try:
        o["job-title"] = (
            soup.find("div", {"class": "top-card-layout__entity-info"})
            .find("a")
            .text.strip()
        )
    except:
        o["job-title"] = None

    try:
        o["text"] = (
            soup.find("section", {"class": "show-more-less-html"})
            .find("div")
            .text.strip()
        )
    except:
        o["text"] = None

    k.append(o)
    o = {}

df = pd.DataFrame(k)
df.to_csv("jobs.csv", index=False, encoding="utf-8")
