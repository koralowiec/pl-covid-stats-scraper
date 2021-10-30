from typing import List
from data.general_data import GeneralData
from data.voivodeship_data import VoivodeshipData


class ScrapedData:

    """ScrapedData represents all data which can be gathered by the scraper."""

    def __init__(
        self,
        general_data: GeneralData = None,
        voivodeships_data: List[VoivodeshipData] = [],
    ):
        self.general_data = general_data
        self.voivodeships_data = voivodeships_data

    def to_dict(self) -> dict:
        general_dict = {}
        if self.general_data is not None:
            general_dict = self.general_data.to_dict()

        voivodeship_dicts: List[dict] = []
        for voivodeship in self.voivodeships_data:
            voivodeship_dicts.append(voivodeship.to_dict())
        voivodeship_dict = {"voivodeships": voivodeship_dicts}

        return general_dict | voivodeship_dict
