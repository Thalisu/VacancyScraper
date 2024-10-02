from bs4 import BeautifulSoup
import requests
import time
import json


class LinkedinScrapper:
    BASE_JOBS_URL = "https://www.linkedin.com/jobs/search?"

    def __init__(
        self,
        keywords,
        location,
        timeframe,
        remote,
    ):
        keywords = f"keywords={keywords}"
        timeframe = f"&f_TPR={timeframe}"
        location = f"&location={location}"
        remote = f"&f_WT={remote}"
        self.url = (
            f"{self.BASE_JOBS_URL}{keywords}{location}{timeframe}{remote}"
        )

    def get_jobs(self, page):
        i = 0
        re = requests.get(self.url)
        while re.status_code != 200 and i < 5:
            re = requests.get(self.url)
            i += 1
            time.sleep(0.2)

        if re.status_code != 200:
            return json.dumps([{"error": "timeout"}], indent=4)

        soup = BeautifulSoup(re.text, "html.parser")
        quotes = soup.findAll("div", attrs={"class": "job-search-card"})
        jobs_dict = [
            {
                "title": quote.find("h3").text.strip(),
                "url": quote.find("a")["href"],
            }
            for quote in quotes
        ]

        return json.dumps(jobs_dict, indent=4)
