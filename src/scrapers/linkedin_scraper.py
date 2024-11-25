from src.utils.constants import (
    LINKEDIN_JOBS_URL,
    LINKEDIN_SIGNIN_URL,
)
from src.utils.config import get_config

from src.selenium.browser import Browser
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
from urllib.parse import quote

import json
import os
import time


class LinkedinJobs:
    output_cookie_dir = "linkedin_cookies.json"
    base_url = "https://www.linkedin.com"
    url: str
    authenticated: bool

    def __init__(self, keywords, location, timeframe, remote):
        keywords = f"keywords={quote(keywords)}"
        location = f"&location={location}"
        timeframe = f"&f_TPR={timeframe}"
        remote = f"&f_WT={remote}"

        self.authenticated = False
        self.url = (
            f"{LINKEDIN_JOBS_URL}{keywords}{location}{timeframe}{remote}"
        )

        self.browser = Browser()

    def get(self, page=0):
        print("Verifying authentication...")
        if not self.__is_authenticated():
            self.__authenticate()

        print("Getting jobs...")
        driver = self.browser.create_driver(headless=True)
        URL = f"{self.url}&start={page * 25}"
        self.browser.get_with_cookies(self.base_url, URL, self.cookies)

        job_list = (
            WebDriverWait(driver, 10)
            .until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "scaffold-layout__list-container")
                )
            )
            .get_attribute("innerHTML")
        )
        html = driver.page_source
        print("Setting up jobs...")
        self.browser.close()

        soup = BeautifulSoup(html, "html.parser")

        no_results = soup.select_one("div.jobs-search-no-results-banner")

        if no_results:
            return []

        soup = BeautifulSoup(job_list, "html.parser")

        job_cards = soup.select(
            "li.jobs-search-results__list-item:not(.jobs-search-results__job-card-search--generic-occludable-area)"
        )
        return self.__get_jobs(job_cards)

    def __authenticate(self):
        driver = self.browser.create_driver(headless=False)
        driver.get(LINKEDIN_SIGNIN_URL)
        driver.find_element(By.ID, "username").send_keys(get_config("USER"))
        driver.find_element(By.ID, "password").send_keys(
            get_config("PASSWORD") + Keys.ENTER
        )
        time.sleep(1)

        is_captcha = "security" in driver.find_element(By.TAG_NAME, "h1").text

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
                title = a.find("strong").text
                url = f"{self.base_url}{a.get('href')}"

                enterprise_container = job.find(
                    "div",
                    attrs={"class": "artdeco-entity-lockup__subtitle"},
                )
                if enterprise_container:
                    enterprise_container = enterprise_container.find("span")
                enterprise = (
                    enterprise_container.text.strip()
                    if enterprise_container
                    else ""
                )

                img = job.find("img")
                if img:
                    img = img.get("src")

                jobs_dict.append(
                    {
                        "title": title,
                        "url": url,
                        "enterprise": enterprise,
                        "img": img,
                    }
                )

        return json.dumps(jobs_dict, indent=4)
