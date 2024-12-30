from seleniumbase import Driver  # type: ignore
from selenium.common.exceptions import InvalidCookieDomainException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.exceptions import InvalidCookiesOrUrl, CantEnsureRequest

import asyncio


class Browser:
    def __init__(self):
        self.driver = None

    def create_driver(self, headless) -> Driver:
        if self.driver:
            return self.driver

        driver = Driver(uc=True, headless=headless)
        self.driver = driver

        return driver

    async def add_cookies_to_domain(self, base_url, cookies: list, retries=2):
        if retries == 0:
            raise InvalidCookiesOrUrl(message="cookies cant be applied")

        self.driver.get(base_url)

        try:
            for cookie in cookies:
                self.driver.add_cookie(cookie)
        except InvalidCookieDomainException:
            await asyncio.sleep(1)
            await self.add_cookies_to_domain(base_url, cookies, retries - 1)
        finally:
            return

    async def ensured_get(self, url):
        self.driver.get(url)

        if not await self.__is_success(url=url):
            raise CantEnsureRequest(f"Failed to ensure connection to {url}")

    async def __is_success(self, url, retries=1, max_retries=5):
        element = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        if "neterror" not in element.text:
            return True

        if not retries <= max_retries:
            return False

        await asyncio.sleep(1)

        self.driver.get(url)
        return self.__is_success(url=url, retries=retries + 1)

    def close(self):
        self.driver.quit()
        self.driver = None
