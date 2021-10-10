import pymongo
from scraped_data import ScrapedData


class Database:
    def __init__(self, connection_url):
        self.client = pymongo.MongoClient(connection_url)
        self.db = self.client.covid
        self.collection = self.db.records

    def is_record_already_saved(self, date: str) -> bool:
        found = self.collection.find_one({"date": date})

        return bool(found)

    def insert_if_not_present(self, data: ScrapedData) -> str:
        is_already_saved = self.is_record_already_saved(data.date)

        if not is_already_saved:
            dict_data = data.to_dict()
            result = self.collection.insert_one(dict_data)
            return result.inserted_id

        return "-1"

    def close_connection(self):
        self.client.close()
