from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from src.utils.config import DRIVER_PATH


class Browser:
    def __init__(self):
        service = Service(executable_path=DRIVER_PATH)
        driver = webdriver.Chrome(service=service)
        self.driver = driver

    def get_driver(self, headless=True):
        if headless:
            self.hide()
        return self.driver

    def hide(self):
        self.driver.set_window_position(-10000, 0)

    def show(self):
        self.driver.set_window_position(0, 0)

    def close(self):
        self.driver.quit()
