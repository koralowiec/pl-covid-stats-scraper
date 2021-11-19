from typing import List
from data.general_data import GeneralData
from data.scraped_data import ScrapedData
from data.voivodeship_data import VoivodeshipData
from database import Database
import os
import sys

from scraps.general import GeneralScraper
from scraps.voivodeship import VoivodeshipScraper


def main():
    mongodb_url = os.environ.get("CONNECTION_URL")
    if mongodb_url is None:
        sys.exit(
            "Provide URL for connecting to MongoDB (via environment variable CONNECTION_URL)"
        )

    database_name = os.environ.get("DB_NAME")
    collection_name = os.environ.get("COL_NAME")

    data = start_scrapers()

    db = Database(mongodb_url, database_name, collection_name)
    result = db.insert_if_not_present(data)

    if result != "-1":
        print("Record saved")
    else:
        print("Record already exists in database")

    db.close_connection()


def start_scrapers() -> ScrapedData:
    print("Starting scrapers...")

    general_scraper = GeneralScraper()
    general_scraper.start_scraping()
    general_data: GeneralData = general_scraper.get_results()
    print("General statistics", general_data)

    voivodeship_scraper = VoivodeshipScraper()
    voivodeship_scraper.start_scraping()
    voivodeship_data: List[VoivodeshipData] = voivodeship_scraper.get_results()
    for v_data in voivodeship_data:
        print(v_data)

    all_data = ScrapedData(
        general_data=general_data, voivodeships_data=voivodeship_data
    )
    return all_data


if __name__ == "__main__":
    main()
