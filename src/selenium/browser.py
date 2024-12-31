from seleniumbase import Driver  # type: ignore
from selenium.webdriver.chrome.webdriver import WebDriver

from selenium.common.exceptions import InvalidCookieDomainException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.exceptions import InvalidCookiesOrUrl, CantEnsureRequest

import asyncio


class Browser:
    def __init__(self) -> None:
        self.driver: WebDriver | None = None

    def create_driver(self, headless: bool) -> WebDriver:
        if self.driver:
            return self.driver

        driver: WebDriver = Driver(uc=True, headless=headless)  # type: ignore
        if not isinstance(driver, WebDriver):
            raise Exception("Failed to create driver")

        self.driver = driver
        return driver

    async def add_cookies_to_domain(
        self, base_url: str, cookies: list[dict[str, str]], retries: int = 2
    ) -> None:
        if retries == 0:
            raise InvalidCookiesOrUrl(message="cookies cant be applied")

        if not self.driver:
            self.driver = self.create_driver(headless=True)

        self.driver.get(base_url)

        try:
            for cookie in cookies:
                self.driver.add_cookie(cookie)  # type: ignore
        except InvalidCookieDomainException:
            await asyncio.sleep(1)
            await self.add_cookies_to_domain(base_url, cookies, retries - 1)
        finally:
            return

    async def ensured_get(self, url: str) -> None:
        if not self.driver:
            self.driver = self.create_driver(headless=True)

        self.driver.get(url)

        if not await self.__is_success(url=url):
            raise CantEnsureRequest(f"Failed to ensure connection to {url}")

    async def __is_success(
        self, url: str, retries: int = 1, max_retries: int = 5
    ) -> bool:

        if not retries <= max_retries:
            return False

        if not self.driver:
            self.driver = self.create_driver(headless=True)

        element = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        if "neterror" not in element.text:
            return True

        await asyncio.sleep(1)

        self.driver.get(url)
        return await self.__is_success(url=url, retries=retries + 1)

    def close(self) -> None:
        if not self.driver:
            return

        self.driver.quit()
        self.driver = None
