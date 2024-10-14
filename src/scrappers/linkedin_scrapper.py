from bs4 import BeautifulSoup
import requests
import time
import json


class LinkedinScrapper:
    BASE_JOBS_URL = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?"

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
        URL = f"{self.url}&start={page * 25}"
        re = requests.get(URL)
        while re.status_code != 200 and i < 5:
            re = requests.get(URL)
            i += 1
            time.sleep(0.2)
        if re.status_code != 200:
            return json.dumps([{"error": "timeout"}], indent=4)

        soup = BeautifulSoup(re.text, "html.parser")
        job_cards = soup.findAll(
            ["div", "a"], attrs={"class": "job-search-card"}
        )
        try:
            jobs_dict = [
                {
                    "title": job.find("h3").text.strip(),
                    "enterprise": job.find("h4").text.strip(),
                    "url": (
                        job.find("a")["href"]
                        if job.find("a")
                        else job.get("href")
                    ),
                    "img": job.find("img")["data-delayed-url"],
                }
                for job in job_cards
            ]
            return json.dumps(jobs_dict, indent=4)
        except TypeError as err:
            return json.dumps([{"TypeError": err.args[0]}], indent=4)
