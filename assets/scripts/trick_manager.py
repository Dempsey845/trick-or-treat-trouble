from cogworks import GameObject
from cogworks.components.script_component import ScriptComponent

from assets.scripts.dog import Dog


class TrickManager(ScriptComponent):
    def __init__(self, house):
        super().__init__()
        self.house = house

    def perform_random_trick(self):
        self.spawn_dog()

    def spawn_dog(self):
        dog = GameObject("Dog", x=self.house.door_pos[0], y=self.house.door_pos[1], scale_x=4, scale_y=4)
        dog.add_component(Dog(self.house.door_pos))

        self.game_object.scene.instantiate_game_object(dog)