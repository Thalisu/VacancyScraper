import undetected_chromedriver as uc  # type: ignore
from selenium.common.exceptions import InvalidCookieDomainException

import sys
import time


class Browser:
    def __init__(self):
        self.driver = None

    def create_driver(self, headless=False):
        if self.driver:
            self.__close()

        driver = uc.Chrome(headless=headless, use_subprocess=False)

        self.driver = driver

        return driver

    def new_cookies(self, cookies: list, retries=2):
        if retries == 0:
            print("cant put cookies")
            sys.exit(0)
        try:
            for cookie in cookies:
                self.driver.add_cookie(cookie)
        except InvalidCookieDomainException:
            time.sleep(1)
            self.new_cookies(cookies, retries - 1)
        finally:
            self.driver.refresh()

    def ensured_get(self, url):
        pass

    def __is_success(self, retries=1, max_retries=3):
        pass

    def __close(self):
        self.driver.quit()
        self.driver = None
