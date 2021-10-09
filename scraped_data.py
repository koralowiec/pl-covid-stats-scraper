class ScrapedData:
    def __init__(
        self,
        total_recovered: int = -1,
        total_death: int = -1,
        total_infected: int = -1,
        daily_recovered: int = -1,
        daily_death: int = -1,
        daily_infected: int = -1,
        date: str = "01.01.1970 00:00",
        scraping_date: str = "01.01.1970 00:00",
    ):
        self.total_recovered = total_recovered
        self.total_death = total_death
        self.total_infected = total_infected
        self.daily_recovered = daily_recovered
        self.daily_death = daily_death
        self.daily_infected = daily_infected
        self.date = date
        self.scraping_date = scraping_date

    def __str__(self):
        return f"""
        Data of scraping: {self.scraping_date}
        Data from: {self.date}
        Total recovered: {self.total_recovered}
        Total death: {self.total_death}
        Total infected: {self.total_infected}
        Daily recovered: {self.daily_recovered}
        Daily death: {self.daily_death}
        Daily infected: {self.daily_infected}
        """

    def to_dict(self) -> dict:
        return {
            "date_of_scrape": self.scraping_date,
            "date": self.date,
            "total": {
                "dead": self.total_death,
                "infected": self.total_infected,
                "recovered": self.total_recovered,
            },
            "daily": {
                "dead": self.daily_death,
                "infected": self.daily_infected,
                "recovered": self.daily_recovered,
            },
        }
