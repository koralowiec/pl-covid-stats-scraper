class VoivodeshipData:

    """VoivodeshipData represents statistics for a voivodeship."""

    def __init__(self, name: str, daily_infected: int = -1, daily_tested: int = -1):
        self.name = name
        self.daily_infected = daily_infected
        self.daily_tested = daily_tested

    def __str__(self):
        return f"""
        Name: {self.name}
        Daily infected: {self.daily_infected}
        Daily tested: {self.daily_tested}
        """

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "daily": {
                "infected": self.daily_infected,
                "tested": self.daily_tested,
            },
        }
