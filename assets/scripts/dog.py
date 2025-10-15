import weakref
import math

from cogworks.components.script_component import ScriptComponent
from cogworks.components.sprite import Sprite


class Dog(ScriptComponent):
    def __init__(self, player_transform):
        super().__init__()
        self.move_speed = 100
        self.player_transform_ref = weakref.ref(player_transform)

    def start(self) -> None:
        sprite = Sprite("images/square.png")
        self.game_object.add_component(sprite)

    def update(self, dt: float) -> None:
        self.calculate_move_direction()
        self.move(dt)

    def calculate_move_direction(self):
        player_transform = self.player_transform_ref()
        if not player_transform:
            return 0, 0

        dog_x, dog_y = self.game_object.transform.get_world_position()
        player_x, player_y = player_transform.get_world_position()

        dx = player_x - dog_x
        dy = player_y - dog_y
        length = math.hypot(dx, dy)
        if length == 0:
            return 0, 0
        return dx / length, dy / length

    def move(self, dt: float):
        dir_x, dir_y = self.calculate_move_direction()
        if dir_x == 0 and dir_y == 0:
            return

        x, y = self.game_object.transform.get_world_position()
        new_x = x + dir_x * self.move_speed * dt
        new_y = y + dir_y * self.move_speed * dt

        self.game_object.transform.set_local_position(new_x, new_y)
