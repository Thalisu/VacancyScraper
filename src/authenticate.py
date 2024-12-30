from seleniumbase import Driver  # type: ignore

from selenium.webdriver.common.keys import Keys
from src.utils.config import get_config
from src.selenium.browser import Browser
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

from src.utils.constants import LINKEDIN_SIGNIN_URL
from src.utils.cookie_encryption import encrypt

import asyncio


class Auth:
    def __init__(self, where: str, driver: Driver = None):
        if where == "linkedin":
            self.__output_cookie_dir = "linkedin_cookies.bin"

        if not driver:
            self.browser = Browser()
            pass

        self.driver = driver

    async def authenticate(self, headless=False):
        if not self.driver:
            self.driver = self.browser.create_driver(headless=headless)

        self.driver.get(LINKEDIN_SIGNIN_URL)
        self.driver.find_element(By.ID, "username").send_keys(
            get_config("USER")
        )
        self.driver.find_element(By.ID, "password").send_keys(
            get_config("PASSWORD") + Keys.ENTER
        )

        await asyncio.sleep(1)

        try:
            is_captcha = (
                "quick" in self.driver.find_element(By.TAG_NAME, "h1").text
            )
        except NoSuchElementException:
            is_captcha = False

        if is_captcha and headless:
            if self.browser:
                self.browser.close()

            return None

        if is_captcha:
            WebDriverWait(self.driver, 20).until_not(
                lambda d: "quick"
                in d.find_element(By.TAG_NAME, "h1").text.lower()
            )

        cookies = self.driver.get_cookies()

        if self.browser:
            self.browser.close()

        encrypt(cookies, self.__output_cookie_dir)
        return cookies
