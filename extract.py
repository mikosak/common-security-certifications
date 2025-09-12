#!/usr/bin/env python

import re
import pandas as pd
import matplotlib.pyplot as plt
import sys

jobs = pd.read_csv(sys.argv[1])
number_of_jobs = len(jobs)
print(f"Processing {number_of_jobs} entries...")
counts = dict()

with open('blacklist.txt') as f:
    blacklist = f.read().splitlines()

def add_count(to_add, dictionary):
    dictionary[to_add] = dictionary.get(to_add, 0) + 1


def extract_and_count(row):

    to_match = r"CASP\+|\b[A-Z]{4,5}\b|(?<=[a-z])[A-Z]{4,5}|[A-Z][a-z]+?\+|\b[A-Z]{2}\b-\b[0-9]{3}\b|\be[A-Z].*?\b|CEH|CCE|\bCAP|EnCE|CFR|GSE|\bCRT|CND"
    found = re.findall(to_match, str(row["text"]))

    for i in found:
        add_count(i, counts)


jobs.apply(extract_and_count, axis=1)

# a lot of posters use Sec+ instead of the actual name
if "Sec+" in counts:
    counts["Security+"] += counts["Sec+"]
    counts.pop("Sec+", None)

for i in blacklist:
    counts.pop(i, None)

to_clean = []
for key, val in counts.items():
    if val < number_of_jobs / 100:
        to_clean.append(key)

for i in to_clean:
    counts.pop(i, None)

counts = dict(sorted(counts.items(), key=lambda item: item[1], reverse=True))
print(counts)

plt.bar(range(10), list(counts.values())[:10], align="center")
plt.xticks(range(10), list(counts.keys())[:10])
plt.show()
