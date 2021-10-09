from scrape import Scraper
from scraped_data import ScrapedData
from database import Database
import os
import sys

mongodb_url = os.environ.get("CONNECTION_URL")
if mongodb_url is None:
    sys.exit(
        "Provide URL for connecting to MongoDB (via environment variable CONNECTION_URL)"
    )

scraper = Scraper()
scraper.start_scraping()
data: ScrapedData = scraper.scraped_data
print("Scraped data", data)

db = Database(mongodb_url)
result = db.insert_if_not_present(data)

if result != "-1":
    print("Record saved")
else:
    print("Record already exists in database")

db.close_connection()
