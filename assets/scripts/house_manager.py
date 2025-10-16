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

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = HouseManager()
        return cls._instance

    def register_house(self, house):
        """Register a house into the manager."""
        self.houses.add(house)

        # Once enough houses are registered, try balancing them
        if len(self.houses) >= (self.minimum_trick + self.minimum_treat):
            self.ensure_minimums()

    def ensure_minimums(self):
        """Ensures at least 10 trick and 10 treat houses exist."""
        if self._balanced:
            return  # Avoid rebalancing repeatedly

        houses = list(self.houses)
        trick_houses = [h for h in houses if h.is_trick]
        treat_houses = [h for h in houses if not h.is_trick]

        # Balance trick houses
        if len(trick_houses) < self.minimum_trick:
            need_more = self.minimum_trick - len(trick_houses)
            available = [h for h in treat_houses if not h.is_trick]
            to_flip = random.sample(available, min(len(available), need_more))
            for h in to_flip:
                h.is_trick = True

        # Balance treat houses
        houses = list(self.houses)  # refresh after flips
        trick_houses = [h for h in houses if h.is_trick]
        treat_houses = [h for h in houses if not h.is_trick]

        if len(treat_houses) < self.minimum_treat:
            need_more = self.minimum_treat - len(treat_houses)
            available = [h for h in trick_houses if h.is_trick]
            to_flip = random.sample(available, min(len(available), need_more))
            for h in to_flip:
                h.is_trick = False

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
