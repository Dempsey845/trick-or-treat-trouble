import random
import weakref
from cogworks.components.script_component import ScriptComponent


class HouseManager(ScriptComponent):
    _instance = None

    def __init__(self):
        super().__init__()
        self.houses = weakref.WeakSet()
        self.minimum_trick = 10
        self.minimum_treat = 10
        self._balanced = False
        self.trick_house_amount = 0
        self.treat_house_amount = 0

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = HouseManager()
        return cls._instance

    def register_house(self, house):
        """Register a house into the manager."""
        self.houses.add(house)

        # Once enough houses are registered, try balancing them
        if len(self.houses) >= 20:
            self.ensure_minimums()

    def ensure_minimums(self):
        if self._balanced:
            return  # Avoid rebalancing repeatedly

        # Balance treat houses
        houses = list(self.houses)

        for i in range(10):
            rand_house = random.choice(houses)
            rand_house.is_trick = True

        for h in houses:
            if h.is_trick:
                self.trick_house_amount += 1
            else:
                self.treat_house_amount += 1

        print(f"Trick house: {self.trick_house_amount} | Treat houses: {self.treat_house_amount}")
        self._balanced = True

    def get_random_trick_house(self):
        trick_houses = [h for h in self.houses if h.is_trick and h.can_knock]
        return random.choice(trick_houses) if trick_houses else None

    def get_random_treat_house(self):
        treat_houses = [h for h in self.houses if not h.is_trick and h.can_knock]
        return random.choice(treat_houses) if treat_houses else None

    def get_random_trick_house_door_pos(self):
        house = self.get_random_trick_house()
        return house.door_pos if house else None

    def get_random_treat_house_door_pos(self):
        house = self.get_random_treat_house()
        return house.door_pos if house else None

    def restart(self):
        self.houses = weakref.WeakSet()
        self._balanced = False
        self.trick_house_amount = 0
        self.treat_house_amount = 0