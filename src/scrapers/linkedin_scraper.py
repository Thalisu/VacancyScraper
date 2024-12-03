from src.utils.constants import (
    LINKEDIN_JOBS_URL,
    LINKEDIN_SIGNIN_URL,
)
from src.utils.config import get_config
from urllib.parse import quote

from src.selenium.browser import Browser
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException
from src.exceptions import MissingKeywords, InvalidCookiesOrUrl, MissingCookies

from bs4 import BeautifulSoup

import json
import os
import time


class LinkedinJobs:
    __output_cookie_dir = "linkedin_cookies.json"
    __base___url = "https://www.linkedin.com"
    __url: str
    __authenticated: bool

    def __init__(
        self,
        keywords,
        location,
        timeframe,
        remote,
    ):
        if not keywords:
            raise MissingKeywords()
        keywords = f"keywords={quote(keywords)}"
        location = f"&location={location}"
        timeframe = f"&f_TPR={timeframe}"
        remote = f"&f_WT={remote}"

        self.__authenticated = False
        self.__url = (
            f"{LINKEDIN_JOBS_URL}{keywords}{location}{timeframe}{remote}"
        )

        self.browser = Browser()

    def get(self, page):
        print("Verifying authentication...")
        if not self.__is_authenticated():
            raise MissingCookies()

        print("Getting jobs...")
        driver = self.browser.create_driver(headless=True)
        __url = f"{self.__url}&start={page * 25}"
        self.browser.get_with_cookies(self.__base___url, __url, self.cookies)

        try:
            job_list = (
                WebDriverWait(driver, 10)
                .until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, "scaffold-layout__list-container")
                    )
                )
                .get_attribute("innerHTML")
            )
        except TimeoutException:
            raise InvalidCookiesOrUrl()
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

    def authenticate(self):
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
        with open(self.__output_cookie_dir, "w") as f:
            json.dump(cookies, f)

        self.cookies = cookies

    def __is_authenticated(self):
        if not os.path.exists(self.__output_cookie_dir):
            return False

        with open(self.__output_cookie_dir, "r") as f:
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
                __url = f"{self.__base___url}{a.get('href')}"

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
                        "__url": __url,
                        "enterprise": enterprise,
                        "img": img,
                    }
                )

        return json.dumps(jobs_dict, indent=4)
