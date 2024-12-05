from src.utils.constants import LINKEDIN_JOBS_URL
from src.utils.cookie_encryption import decrypt

from urllib.parse import quote

from src.selenium.browser import Browser
from src.authenticate import Auth
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException
from src.exceptions import MissingKeywords, InvalidCookiesOrUrl, MissingCookies

from bs4 import BeautifulSoup

import os


class LinkedinJobs:
    __output_cookie_dir = "linkedin_cookies.bin"
    __base_url = "https://www.linkedin.com"
    __url: str

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

        self.__url = (
            f"{LINKEDIN_JOBS_URL}{keywords}{location}{timeframe}{remote}"
        )

        self.auth = Auth("linkedin")
        self.browser = Browser()

    def get(self, page):
        # print("Verifying authentication...")
        if not self.__is_authenticated():
            # print("Trying headless Authentication...")
            self.__authenticate()
        else:
            self.cookies = decrypt(self.__output_cookie_dir)

        # print("Getting jobs...")
        html = self.__get_jobs_html(page)

        # print("Setting up jobs...")
        soup = BeautifulSoup(html[0], "html.parser")

        no_results = soup.select_one("div.jobs-search-no-results-banner")

        if no_results:
            return []

        soup = BeautifulSoup(html[1], "html.parser")

        job_cards = soup.select("li.scaffold-layout__list-item")
        return self.__get_jobs(job_cards)

    def __get_jobs_html(self, page, retries=1):
        driver = self.browser.create_driver(headless=False)
        url = f"{self.__url}&start={page * 25}"
        self.browser.get_with_cookies(self.__base_url, url, self.cookies)

        try:
            job_list = (
                WebDriverWait(driver, 10)
                .until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, "scaffold-layout__list")
                    )
                )
                .get_attribute("innerHTML")
            )
        except TimeoutException:
            self.browser.close()

            if not retries:
                raise InvalidCookiesOrUrl()

            self.__authenticate()
            return self.__get_jobs_html(page, retries=retries - 1)

        html = driver.page_source
        self.browser.close()
        return [html, job_list]

    def __authenticate(self):
        self.cookies = self.auth.authenticate(headless=True)
        if not self.cookies:
            raise MissingCookies()

    def __is_authenticated(self):
        cookie_path = self.__output_cookie_dir

        if not os.path.exists(cookie_path):
            return False

        cookies = decrypt(cookie_path)
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
                url = f"{self.__base_url}{a.get('href')}"

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
                        "title": f"{title}",
                        "url": f"{url}",
                        "enterprise": f"{enterprise}",
                        "img": f"{img}",
                    }
                )

        return jobs_dict
