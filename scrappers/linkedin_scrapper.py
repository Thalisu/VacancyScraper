from bs4 import BeautifulSoup
import requests


class LinkedinScrapper:
    BASE_JOBS_URL = "https://www.linkedin.com/jobs/search?"

    def __init__(
        self,
        keywords,
        location="Brazil",
        timeframe="r86400",
        remote="1%2C2%2C3",
    ):
        keywords = f"keywords={keywords}"
        timeframe = f"&f_TPR={timeframe}"
        location = f"&location={location}"
        remote = f"&f_WT={remote}"
        self.url = (
            f"{self.BASE_JOBS_URL}{keywords}{location}{timeframe}{remote}"
        )

    def get_jobs(self, page):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.text, "html.parser")
        quotes = soup.findAll("div", attrs={"class": "job-search-card"})
        jobs = [
            (quote.find("h3").text.strip(), quote.find("a")["href"])
            for quote in quotes
        ]
        return jobs
