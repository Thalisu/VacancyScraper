import sys
from scrappers.linkedin_scrapper import get_linkedin_jobs

keywords = sys.argv[1] or "desenvolvedor"
location = sys.argv[2] or "Brazil"
timeframe = sys.argv[3] or "r86400"
remote = sys.argv[4] or "1%2C2%2C3"
page = sys.argv[5] or 0

print(get_linkedin_jobs(keywords, location, timeframe, remote, page))
