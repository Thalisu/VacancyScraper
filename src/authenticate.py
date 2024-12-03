from selenium.webdriver.common.keys import Keys
from src.utils.config import get_config
from src.selenium.browser import Browser
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

from src.utils.constants import LINKEDIN_SIGNIN_URL

import time
import json


class Auth:
    def __init__(self, where):
        if where == "linkedin":
            self.__output_cookie_dir = "linkedin_cookies.json"

        self.browser = Browser()

    def authenticate(self):
        driver = self.browser.create_driver(headless=False)
        driver.get(LINKEDIN_SIGNIN_URL)
        driver.find_element(By.ID, "username").send_keys(get_config("USER"))
        driver.find_element(By.ID, "password").send_keys(
            get_config("PASSWORD") + Keys.ENTER
        )
        time.sleep(1)
        try:
            is_captcha = (
                "security" in driver.find_element(By.TAG_NAME, "h1").text
            )
        except NoSuchElementException:
            is_captcha = False

        if is_captcha:
            WebDriverWait(driver, 20).until_not(
                lambda d: "security"
                in d.find_element(By.TAG_NAME, "h1").text.lower()
            )

        cookies = driver.get_cookies()
        self.browser.close()

        with open(self.__output_cookie_dir, "w") as f:
            json.dump(cookies, f)
