#!/usr/bin/env python

import re
import pandas as pd
import matplotlib.pyplot as plt

jobs = pd.read_csv('jobs.csv')
number_of_jobs = len(jobs)
print(f"Processing {number_of_jobs} entries...")
counts = dict()
blacklist = ["SIEM", "NIST", "HMRC", "GDPR", "FTSE", "MHCLG", "CSOC", "STEM", "CISO", "EUSS", "ISMS", "DBSC", "ASOS", "NCSC", "DORA", "STRAP", "CREST", "KINTO", "UBDS", "GIAC", "KPMG", "CHECK", "IDEAL", "WILL", "FULL", "COST", "CEMA", "SAST", "DAST", "SANS", "FREE", "MITRE", "OWASP", "CSPM", "EMSOU", "CSIRT", "DFIR", "MSSP", "DHCP", "JCKP", "IASME", "ITIL", "ITSM", "CE+", "CODE", "PHIA", "CERT", "REST", "SOAP", "LGBTQ", "TPRM", "SOAR", "CFGI", "OSINT", "RAND", "GCSE", "TPDD", "EMEA", "ASDA", "APPLY", "NATO"]

def add_count(to_add, dictionary):
   dictionary[to_add] = dictionary.get(to_add, 0) + 1

def extract_and_count(row):
    
    to_match = r"\b[A-Z]{4,5}\b|\b[A-Za-z]+?\+|CEH"
    found = re.findall(to_match, str(row["text"]))

    for i in found:
        add_count(i, counts)

jobs.apply(extract_and_count, axis = 1)

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

plt.bar(range(10), list(counts.values())[:10], align='center')
plt.xticks(range(10), list(counts.keys())[:10])
plt.show()
