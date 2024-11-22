from src.utils.constants import (
    LINKEDIN_JOBS_URL,
    LINKEDIN_SIGNIN_URL,
)
from src.utils.config import USER, PASSWORD

from src.selenium.browser import Browser
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

import json
import os


class LinkedinJobs:
    output_cookie_dir = "linkedin_cookies.json"
    base_url = "https://www.linkedin.com"
    url: str
    authenticated: bool

    def __init__(self, keywords, location, timeframe, remote):
        keywords = f"keywords={keywords}"
        location = f"&location={location}"
        timeframe = f"&f_TPR={timeframe}"
        remote = f"&f_WT={remote}"

        self.authenticated = False
        self.url = (
            f"{LINKEDIN_JOBS_URL}{keywords}{location}{timeframe}{remote}"
        )

        self.browser = Browser()

    def get(self, page=0):
        if not self.__is_authenticated():
            self.__authenticate()

        driver = self.browser.create_driver(headless=False)
        URL = f"{self.url}&start={page * 25}"
        driver.get(URL)
        self.browser.new_cookies(self.cookies)

        html = (
            WebDriverWait(driver, 10)
            .until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "scaffold-layout__list-container")
                )
            )
            .get_attribute("innerHTML")
        )

        soup = BeautifulSoup(html, "html.parser")

        job_cards = soup.select(
            "li.jobs-search-results__list-item:not(.jobs-search-results__job-card-search--generic-occludable-area)"
        )
        return self.__get_jobs(job_cards)

    def __authenticate(self):
        driver = self.browser.create_driver()
        driver.get(LINKEDIN_SIGNIN_URL)
        driver.find_element(By.ID, "username").send_keys(USER)
        driver.find_element(By.ID, "password").send_keys(PASSWORD + Keys.ENTER)

        is_captcha = WebDriverWait(driver, 1).until(
            lambda d: "security"
            in d.find_element(By.TAG_NAME, "h1").text.lower()
        )

        if is_captcha:
            WebDriverWait(driver, 20).until_not(
                lambda d: "security"
                in d.find_element(By.TAG_NAME, "h1").text.lower()
            )

        cookies = driver.get_cookies()
        with open(self.output_cookie_dir, "w") as f:
            json.dump(cookies, f)

        self.cookies = cookies

    def __is_authenticated(self):
        if not os.path.exists(self.output_cookie_dir):
            return False

        with open(self.output_cookie_dir, "r") as f:
            cookies = json.load(f)
            if not cookies:
                return False

            self.cookies = cookies
            return True

    def __get_jobs(self, job_cards):
        jobs_dict = []
        with open("random.html", "w") as f:
            for job in job_cards:
                f.write(str(job))
                a = job.find("a")
                if not a:
                    continue
                span = job.find(
                    "span",
                    attrs={"class": "job-card-container__primary-description"},
                )
                img = job.find("img")

                jobs_dict.append(
                    {
                        "title": a.find("strong").text if a else "",
                        "enterprise": span.text.strip() if span else "",
                        "url": (
                            (f"{self.base_url}{a.get('href')}") if a else ""
                        ),
                        "img": img.get("src") if img else "",
                    }
                )

        return json.dumps(jobs_dict, indent=4)


TEST = LinkedinJobs("desenvolvedor", "Brazil", "r86400", "1%2C2%2C3")
print(TEST.get())
