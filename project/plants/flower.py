from project.plants.base_plant import BasePlant


class Flower(BasePlant):
    VALID_BLOOMING_SEASON = ["Spring", "Summer", "Fall", "Winter"]

    def __init__(self, name: str, price: float, water_needed: int, blooming_season):
        super().__init__(name, price, water_needed)
        self.blooming_season = blooming_season

    @property
    def blooming_season(self):
        return self.__blooming_season

    @blooming_season.setter
    def blooming_season(self, value):
        if not value in self.VALID_BLOOMING_SEASON:
            raise ValueError("Blooming season must be a valid one!")
        self.__blooming_season = value

    def plant_details(self):
        return f"Flower: {self.name}, Price: {self.price:.2f}," \
               f" Watering: {self.water_needed}ml, Blooming Season: {self.blooming_season}"