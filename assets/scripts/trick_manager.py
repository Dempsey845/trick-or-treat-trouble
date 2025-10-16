import random

from cogworks import GameObject
from cogworks.components.script_component import ScriptComponent
from cogworks.pygame_wrappers.window import Window

from assets.scripts.dog import Dog
from assets.scripts.level_manager import LevelManager
from assets.scripts.witch_head import WitchHead


class TrickManager(ScriptComponent):
    def __init__(self, house):
        super().__init__()
        self.house = house
        self.tricks = [self.spawn_dog, self.spawn_witch]

    def perform_random_trick(self):
        random_callable = random.choice(self.tricks)
        random_callable()

    def spawn_dog(self):
        dog = GameObject("Dog", x=self.house.door_pos[0], y=self.house.door_pos[1], scale_x=4, scale_y=4)
        dog.add_component(Dog(self.house.door_pos))

        self.game_object.scene.instantiate_game_object(dog)

    def spawn_witch(self):
        window_width, window_height = Window.get_instance().get_size()

        witch_head = GameObject("Witch Head", z_index=50, x=window_width / 2, y=window_height / 2)
        witch_head.add_component(WitchHead())

        self.game_object.scene.instantiate_game_object(witch_head)

        lm = LevelManager.get_instance()
        lm.invert_player_movement(7)