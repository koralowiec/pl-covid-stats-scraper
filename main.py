from data.general_data import GeneralData
from data.scraped_data import ScrapedData
from database import Database
import os
import sys

from scraps.general import GeneralScraper


def main():
    mongodb_url = os.environ.get("CONNECTION_URL")
    if mongodb_url is None:
        sys.exit(
            "Provide URL for connecting to MongoDB (via environment variable CONNECTION_URL)"
        )

    data = start_scrapers()

    db = Database(mongodb_url)
    result = db.insert_if_not_present(data)

    if result != "-1":
        print("Record saved")
    else:
        print("Record already exists in database")

    db.close_connection()


def start_scrapers() -> ScrapedData:
    general_scraper = GeneralScraper()
    general_scraper.start_scraping()
    general_data: GeneralData = general_scraper.get_results()
    print("General statistics", general_data)

    all_data = ScrapedData(general_data=general_data)
    return all_data


if __name__ == "__main__":
    main()
