from typing import Union
import pymongo

from data.scraped_data import ScrapedData


class Database:
    def __init__(
        self,
        connection_url: str,
        database_name: Union[str, None],
        collection_name: Union[str, None],
    ):
        self.client = pymongo.MongoClient(connection_url)

        if database_name:
            self.db = self.client[database_name]
        else:
            self.db = self.client.covid

        if collection_name:
            self.collection = self.db[collection_name]
        else:
            self.collection = self.db.records

    def is_record_already_saved(self, date: str) -> bool:
        separated_date = date.split(" ")[0]
        found = self.collection.find_one({"date": {"$regex": f"^{separated_date}"}})
        return bool(found)

    def insert_if_not_present(self, data: ScrapedData) -> str:
        is_already_saved = self.is_record_already_saved(data.general_data.date)

        if not is_already_saved:
            dict_data = data.to_dict()
            result = self.collection.insert_one(dict_data)
            return result.inserted_id

        return "-1"

    def close_connection(self):
        self.client.close()
