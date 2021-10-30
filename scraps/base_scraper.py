from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options


class BaseScraper:
    wait_sec = 90

    def __init__(self, url: str, headless: bool = True):
        self.url = url
        options = Options()
        options.headless = headless
        self.driver = webdriver.Firefox(options=options)

    def start_scraping(self):
        self.driver.get(self.url)
        self.scrape()
        self.driver.close()

    def scrape(self):
        pass

    def get_value_by_xpath(self, xpath_selector: str) -> str:
        return self.driver.find_element_by_xpath(xpath_selector).text

    def get_number_by_xpath(self, xpath_selector: str) -> int:
        string_number_with_commas = self.get_value_by_xpath(xpath_selector)
        return int(string_number_with_commas.replace(",", ""))

    def wait_unitl_xpath_element_is_shown(self, selector: str):
        self.wait_unitl_element_is_shown(locator_strategy=By.XPATH, selector=selector)

    def wait_unitl_css_element_is_shown(self, selector: str):
        self.wait_unitl_element_is_shown(
            locator_strategy=By.CSS_SELECTOR, selector=selector
        )

    def wait_unitl_element_is_shown(self, locator_strategy, selector):
        wait = WebDriverWait(self.driver, self.wait_sec)
        wait.until(EC.visibility_of_element_located((locator_strategy, selector)))
