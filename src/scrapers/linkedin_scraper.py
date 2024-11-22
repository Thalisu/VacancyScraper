from src.utils.constants import (
    LINKEDIN_JOBS_URL,
    LINKEDIN_AUTH_URL,
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

# https://www.linkedin.com/voyager/api/voyagerJobsDashJobCards?decorationId=com.linkedin.voyager.dash.deco.jobs.search.JobSearchCardsCollectionLite-83&count=7&q=jobSearch&query=(currentJobId:4045330029,origin:SWITCH_SEARCH_VERTICAL,keywords:( "backend" OR "back end" OR "back-end" ) AND ( "jr" OR junior ) AND ( express OR django OR flask OR node OR nest ) NOT senior,spellCorrectionEnabled:true)&servedEventEnabled=false&start=0


class LinkedinJobs:
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
        self.driver = self.browser.get_driver(headless=True)

    def get(self, page=0):
        if not self.authenticated:
            self.__authenticate()

        URL = f"{self.url}&start={page * 25}"
        self.driver.get(URL)
        html = (
            WebDriverWait(self.driver, 10)
            .until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "scaffold-layout__list-container")
                )
            )
            .get_attribute("innerHTML")
        )

        soup = BeautifulSoup(html, "html.parser")

        job_cards = soup.find("li")
        print(job_cards)
        return

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

    def __authenticate(self):
        self.driver.get(LINKEDIN_SIGNIN_URL)
        self.driver.find_element(By.ID, "username").send_keys(USER)
        self.driver.find_element(By.ID, "password").send_keys(
            PASSWORD + Keys.ENTER
        )

        is_captcha = WebDriverWait(self.driver, 1).until(
            EC.presence_of_element_located((By.ID, "captcha-internal"))
        )

        if is_captcha:
            WebDriverWait(self.driver, 20).until_not(
                EC.presence_of_element_located((By.ID, "captcha-internal"))
            )


TEST = LinkedinJobs("desenvolvedor", "Brazil", "r86400", "1%2C2%2C3")
TEST.get()
