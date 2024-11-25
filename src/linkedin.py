import sys
from scrapers.linkedin_scraper import LinkedinJobs

keywords = sys.argv[1]
if not keywords:
    print("Keywords are required")
    sys.exit(0)
location = sys.argv[2] or "Brazil"
timeframe = sys.argv[3] or "r86400"
remote = sys.argv[4] or "1%2C2%2C3"
page = sys.argv[5] or 0

jobs = LinkedinJobs(keywords, location, timeframe, remote)

job_list = jobs.get(page)

print(job_list)
