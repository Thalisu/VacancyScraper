from seleniumbase import Driver  # type: ignore
from selenium.common.exceptions import InvalidCookieDomainException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import sys
import time


class Browser:
    def __init__(self):
        self.driver = None

    def create_driver(self, headless=False):
        if self.driver:
            self.close()

        driver = Driver(uc=True, headless=headless)
        self.driver = driver

        return driver

    def get_with_cookies(
        self, base_url, url, cookies: list, ensured=True, retries=2
    ):
        self.driver.get(base_url)

        if retries == 0:
            print("cant put cookies")
            sys.exit(0)

        try:
            for cookie in cookies:
                self.driver.add_cookie(cookie)
        except InvalidCookieDomainException:
            time.sleep(1)
            self.get_with_cookies(base_url, url, cookies, ensured, retries - 1)
        finally:
            if ensured:
                self.ensured_get(url=url)
            else:
                self.driver.get(url)

    def ensured_get(self, url):
        self.driver.get(url)

        if not self.__is_success(url=url):
            print("cant get")
            sys.exit(0)

    def __is_success(self, url, retries=1, max_retries=5):
        element = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        if "neterror" not in element.get_attribute("class").split():
            return True

        if not retries <= max_retries:
            return False

        time.sleep(retries * 0.5)
        self.driver.get(url)
        return self.__is_success(url=url, retries=retries + 1)

    def close(self):
        self.driver.quit()
        self.driver = None
