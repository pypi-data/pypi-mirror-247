from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os
from selenium.webdriver.chrome.options import Options
from random import randint
import time

class SeleniumUtils:
    def __init__(self, min_wait_time, max_wait_time):
        self.min_wait_time = min_wait_time
        self.max_wait_time = max_wait_time
    def launch_browser(self,
                       url: str,
                       headless: bool,
                       local_identifier: [str, None],
                       prod_identifier: [str, None],
                       chrome_driver_path: [str, None]):
        chrome_options = Options()
        chrome_options.add_argument("start-maximized");
        if headless:
            chrome_options.add_argument("--headless=new")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_experimental_option("detach", True)
        if (prod_identifier in os.getcwd() or local_identifier in os.getcwd()) and chrome_driver_path is not None :
            service = Service(executable_path=chrome_driver_path)
        else:
            service = Service()

        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(url)
        driver.maximize_window()  # For maximizing window
        driver.implicitly_wait(randint(self.min_wait_time, self.max_wait_time))
        time.sleep(randint(self.min_wait_time, self.max_wait_time))
        return driver
