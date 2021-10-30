from time import sleep


class VoivodeshipScraper:
    url = "https://wojewodztwa-rcb-gis.hub.arcgis.com/"
    wait_sec = 90

    infected_number_selector = '//section[@id="ember59"]'
    infected_stats_voivodeship_list = f"{infected_number_selector}//*[local-name() = 'svg']//*[contains(@aria-label, 'Liczba zakażeń')]"
    # infected_stats_voivodeship_list = f"//*[contains(@aria-label, 'Liczba zakażeń')]"

    def __init__(self, driver):
        self.driver = driver

    def asd(self):
        self.driver.get(self.url)
        print("asd start")
        sleep(30.0)
        y = self.driver.find_elements_by_xpath("//section")
        print(y)
        for i in y:
            print(i)
            print(i.get_attribute("id"))
        x = self.driver.find_elements_by_xpath(self.infected_stats_voivodeship_list)
        print(x)
        for v in x:
            print(v.get_attribute("aria-label"))
        self.driver.close()
