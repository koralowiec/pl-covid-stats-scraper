from data.general_data import GeneralData
from datetime import datetime
from scraps.base_scraper import BaseScraper


class GeneralScraper(BaseScraper):
    url = "https://rcb-gis.maps.arcgis.com/apps/dashboards/fc789be735144881a5ea2c011f6c9265"

    green_heart_image_url = "https://rcb-gis.maps.arcgis.com/sharing/rest/content/items/6044a0d70784489b8a1f02f20c518a35/data"
    green_heart_image_selector = f'img[src="{green_heart_image_url}"]'

    data_date_selector = "(//full-container//span//strong)[1]"

    number_selector_template = "(//full-container//span[img])[{i}]"
    total_recovered_img_selector = number_selector_template.format(i=1)
    total_death_img_selector = number_selector_template.format(i=2)
    total_infected_img_selector = number_selector_template.format(i=3)

    daily_special_selector_template = (
        "(//full-container//span[preceding-sibling::img])[{i}]"
    )
    daily_death_img_selector = number_selector_template.format(i=5)
    daily_infected_img_selector = daily_special_selector_template.format(i=1)
    daily_recovered_img_selector = daily_special_selector_template.format(i=2)

    def __init__(self, headless: bool = True):
        self.scraped_data = GeneralData()
        super().__init__(self.url, headless)

    def scrape(self):
        print("Scraping general statistics...")
        self.wait_unitl_numbers_are_shown()
        self.set_date_of_scraping()
        self.scrape_date()
        self.scrape_numbers()

    def get_results(self) -> GeneralData:
        return self.scraped_data

    def scrape_numbers(self):
        self.scraped_data.total_infected = self.get_number_by_xpath(
            self.total_infected_img_selector
        )
        self.scraped_data.total_recovered = self.get_number_by_xpath(
            self.total_recovered_img_selector
        )
        self.scraped_data.total_death = self.get_number_by_xpath(
            self.total_death_img_selector
        )

        self.scraped_data.daily_infected = self.get_number_by_xpath(
            self.daily_infected_img_selector
        )
        self.scraped_data.daily_recovered = self.get_number_by_xpath(
            self.daily_recovered_img_selector
        )
        self.scraped_data.daily_death = self.get_number_by_xpath(
            self.daily_death_img_selector
        )

    def scrape_date(self) -> str:
        date_of_available_data = self.get_value_by_xpath(self.data_date_selector)
        self.scraped_data.date = date_of_available_data
        return date_of_available_data

    def set_date_of_scraping(self):
        current_date = datetime.today()
        self.scraped_data.scraping_date = str(current_date)

    def wait_unitl_numbers_are_shown(self):
        self.wait_unitl_css_element_is_shown(self.green_heart_image_selector)
