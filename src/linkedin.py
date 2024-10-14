import sys
from scrappers.linkedin_scrapper import LinkedinScrapper

keywords = sys.argv[1] or "desenvolvedor"
location = sys.argv[2] or "Brazil"
timeframe = sys.argv[3] or "r86400"
remote = sys.argv[4] or "1%2C2%2C3"
page = sys.argv[5] or 0

SCRAPPER = LinkedinScrapper(keywords, location, timeframe, remote)

print(SCRAPPER.get_jobs(page))
