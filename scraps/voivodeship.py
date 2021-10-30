from typing import List, Tuple, Union

from selenium.webdriver.remote.webelement import WebElement
from data.voivodeship_data import VoivodeshipData
from scraps.base_scraper import BaseScraper


class VoivodeshipScraper(BaseScraper):
    url = "https://wojewodztwa-rcb-gis.hub.arcgis.com/"

    daily_infected_chart_seletor = (
        "//section[@id='ember59']//div[@class='amcharts-chart-div']"
    )
    daily_infected_list_selector = (
        f"{daily_infected_chart_seletor}//*[contains(@aria-label, 'Liczba zakażeń')]"
    )
    daily_tested_chart_selector = (
        "//section[@id='ember67']//div[@class='amcharts-chart-div']"
    )
    daily_tested_list_selector = f"{daily_tested_chart_selector}//*[contains(@aria-label, 'Liczba wykonanych testów')]"

    attribute_with_infromation = "aria-label"

    def __init__(self, headless: bool = True):
        self.voivodeships_data: List[VoivodeshipData] = []
        super().__init__(self.url, headless)

    def scrape(self):
        print("Scraping voivodeships statistics...")
        self.wait_unitl_charts_are_shown()
        self.scrape_daily_stats_from_charts()

    def get_results(self) -> List[VoivodeshipData]:
        return self.voivodeships_data

    def scrape_daily_stats_from_charts(self):
        daily_infected_elements: List[WebElement] = self.driver.find_elements_by_xpath(
            self.daily_infected_list_selector
        )

        temp_voivodeship_data: dict = {}
        for e in daily_infected_elements:
            attr = e.get_attribute(self.attribute_with_infromation)
            v_name, v_tested = self.extract_voivodeship_data_from_attribute(attr)

            if v_name is not None and v_tested is not None:
                temp_dict = {"infected": v_tested}
                temp_voivodeship_data[v_name] = temp_dict

        daily_tested_elements: List[WebElement] = self.driver.find_elements_by_xpath(
            self.daily_tested_list_selector
        )

        for e in daily_tested_elements:
            attr = e.get_attribute(self.attribute_with_infromation)
            v_name, v_tested = self.extract_voivodeship_data_from_attribute(attr)

            if v_name is not None and v_tested is not None:
                temp_voivodeship_data[v_name]["tested"] = v_tested

        self.voivodeships_data = self.convert_dict_with_daily_stats(
            temp_voivodeship_data
        )

    def extract_voivodeship_data_from_attribute(
        self, value: str
    ) -> Union[Tuple[str, int], Tuple[None, None]]:
        splited = value.split(" ")
        if len(splited) not in [4, 5]:
            return None, None

        voivodeship_name = splited[-2:-1][0]
        voivodeship_value_str = splited[-1:][0]
        voivodeship_value = self.str_number_with_comma_to_int(voivodeship_value_str)

        return voivodeship_name, voivodeship_value

    def convert_dict_with_daily_stats(
        self, voivodeship_data_dict: dict
    ) -> List[VoivodeshipData]:
        data: List[VoivodeshipData] = []

        for v_name in voivodeship_data_dict:
            v_infected = voivodeship_data_dict[v_name]["infected"]
            v_tested = voivodeship_data_dict[v_name]["tested"]

            v_data = VoivodeshipData(
                name=v_name, daily_infected=v_infected, daily_tested=v_tested
            )
            data.append(v_data)

        return data

    def wait_unitl_charts_are_shown(self):
        self.wait_unitl_xpath_element_is_shown(self.daily_infected_chart_seletor)
        self.wait_unitl_xpath_element_is_shown(self.daily_tested_chart_selector)
