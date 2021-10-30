class VoivodeshipData:

    """VoivodeshipData represents statistics for a voivodeship."""

    def __init__(self, daily_infected: int = -1, daily_tested: int = -1):
        self.daily_infected = daily_infected
        self.daily_tested = daily_tested

    def __str__(self):
        return f"""
        Daily infected: {self.daily_infected}
        Daily tested: {self.daily_tested}
        """

    def to_dict(self) -> dict:
        return {
            "daily": {
                "infected": self.daily_infected,
                "tested": self.daily_tested,
            },
        }
