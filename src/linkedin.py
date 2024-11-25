import sys
from src.scrapers.linkedin_scraper import LinkedinJobs

keywords = sys.argv[1]
if not keywords:
    print("Keywords are required")
    sys.exit(0)
try:
    location = sys.argv[2]
except IndexError:
    location = "Brazil"

try:
    timeframe = sys.argv[3]
except IndexError:
    timeframe = "r86400"

try:
    remote = sys.argv[4]
except IndexError:
    remote = "1%2C2%2C3"

try:
    page = sys.argv[5]
except IndexError:
    page = 0

jobs = LinkedinJobs(keywords, location, timeframe, remote)

job_list = jobs.get(page)

print(job_list)
