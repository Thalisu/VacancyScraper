from src.utils.constants import LINKEDIN_JOBS_URL
from src.utils.cookie_encryption import decrypt
from src.models import error, responses

from urllib.parse import quote

from src.selenium.browser import Browser
from src.authenticate import Auth
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException
from src.exceptions import (
    InvalidCookiesOrUrl,
    MissingCookies,
    CantEnsureRequest,
)

from src.schemas.linkedin import JobRequests

from src.models.job import Jobs

from bs4 import BeautifulSoup
from bs4.element import Tag

import os


class LinkedinJobs:
    __cookies: list[dict[str, str]] | None
    __output_cookie_dir: str = "linkedin_cookies.bin"
    __base_url: str = "https://www.linkedin.com"
    __url: str

    def __init__(self, jobRequests: JobRequests) -> None:
        keywords: list[str] = []
        locations = timeframes = remotes = pages = keywords

        self.keywords: list[str] = []
        for jobRequest in jobRequests:
            self.keywords.append(jobRequest.keywords)
            keywords.append(f"keywords={quote(jobRequest.keywords)}")
            locations.append(f"&location={jobRequest.location}")
            timeframes.append(f"&f_TPR={jobRequest.timeframe}")
            remotes.append(f"&f_WT={jobRequest.remote}")
            pages.append(f"&start={jobRequest.page * 25}")

        self.__urls = [
            f"{LINKEDIN_JOBS_URL}{keyword}{location}{timeframe}{remote}{page}"
            for keyword, location, timeframe, remote, page in zip(
                keywords, locations, timeframes, remotes, pages
            )
        ]

        self.browser = Browser()
        self.browser.create_driver(headless=False)
        self.auth = Auth("linkedin", self.browser.driver)

    async def get(self) -> list[responses.Data]:
        # print("Verifying authentication...")
        if not self.__is_authenticated():
            # print("Trying headless Authentication...")
            await self.__authenticate()

        if not self.__cookies:
            raise MissingCookies()

        await self.browser.add_cookies_to_domain(
            self.__base_url, self.__cookies
        )

        # print("Getting jobs...")
        data: list[responses.Data] = []
        for url, keyword in zip(self.__urls, self.keywords):
            base_data: responses.Data = {
                "keywords": keyword,
                "jobs": [],
                "error": None,
            }

            html = await self.__get_jobs_html(url)

            soup = BeautifulSoup(html["page"], "html.parser")

            no_results = soup.select_one("div.jobs-search-no-results-banner")

            if no_results:
                error_dict: error.ErrorDetail = {
                    "status_code": 404,
                    "message": "no results",
                }
                base_data["error"] = error_dict
                data.append(base_data)
            else:
                base_data["jobs"] = self.__format_jobs(html["job_list"])
                data.append(base_data)

        self.browser.close()
        return data

    async def __get_jobs_html(
        self, url: str, retries: int = 1
    ) -> dict[str, str]:
        driver = self.browser.get_driver()

        try:
            await self.browser.ensured_get(url)
        except CantEnsureRequest:
            return {"page": "", "job_list": ""}

        try:
            job_list = (
                WebDriverWait(driver, 10)
                .until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, "scaffold-layout__list")
                    )
                )
                .get_attribute("innerHTML")  # type: ignore
            )
        except TimeoutException:
            if not retries:
                self.browser.close()
                raise InvalidCookiesOrUrl()

            await self.__authenticate()
            return await self.__get_jobs_html(url, retries=retries - 1)

        page = driver.page_source
        return {"page": page, "job_list": job_list or ""}

    async def __authenticate(self) -> None:
        self.__cookies = await self.auth.authenticate()

        if not self.__cookies:
            self.browser.close()
            raise MissingCookies()

    def __is_authenticated(self) -> bool:
        cookie_path = self.__output_cookie_dir

        if not os.path.exists(cookie_path):
            return False

        cookies = decrypt(cookie_path)
        if not cookies:
            return False

        self.__cookies = cookies
        return True

    def __format_jobs(self, job_list_html: str) -> Jobs:
        soup = BeautifulSoup(job_list_html, "html.parser")

        job_cards = soup.select("li.scaffold-layout__list-item")

        jobs_dict: Jobs = []
        for job in job_cards:
            a = job.find("a")
            if not isinstance(a, Tag):
                continue
            strong = a.find("strong")
            if not isinstance(strong, Tag):
                continue

            title = strong.get_text(strip=True)
            url = f"{self.__base_url}{a.attrs["href"]}"

            div = job.find(
                "div",
                attrs={"class": "artdeco-entity-lockup__subtitle"},
            )

            enterprise_container = None
            enterprise = None
            if isinstance(div, Tag):
                enterprise_container = div.find("span")

            if enterprise_container and isinstance(enterprise_container, Tag):
                enterprise = enterprise_container.get_text(strip=True)

            img = None
            img_tag = job.find("img")
            if isinstance(img_tag, Tag):
                img = img_tag.attrs["src"]

            time_container = job.find("time")
            state = None
            if isinstance(time_container, Tag):
                state = time_container.get_text(strip=True)

            if not state:
                state_container = job.find(
                    "li",
                    attrs={"class": "job-card-container__footer-job-state"},
                )
                if isinstance(state_container, Tag):
                    state = state_container.get_text(strip=True)

            location = None
            location_container = job.find(
                "ul",
                attrs={"class": "job-card-container__metadata-wrapper"},
            )
            if isinstance(location_container, Tag):
                location = location_container.get_text(strip=True)

            jobs_dict.append(
                {
                    "title": title,
                    "url": url,
                    "enterprise": enterprise if enterprise else "",
                    "img": img if img else "",
                    "state": state if state else "",
                    "location": location if location else "",
                }
            )

        return jobs_dict
