import math

from cogworks.components.script_component import ScriptComponent
from cogworks.components.sprite import Sprite
from cogworks.components.trigger_collider import TriggerCollider


class Stick(ScriptComponent):
    def __init__(self, player_x, player_y, speed):
        super().__init__()
        self.player_x = player_x
        self.player_y = player_y
        self.move_direction = (0, 0)
        self.speed = speed
        self.lifetime = 2.0
        self.timer = 0.0

    def start(self) -> None:
        self.game_object.add_component(Sprite("images/stick.png"))
        self.game_object.add_component(TriggerCollider(layer="Projectile", layer_mask=["Player"]))

        x, y = self.game_object.transform.get_local_position()

        dx = self.player_x - x
        dy = self.player_y - y

        length = math.hypot(dx, dy)
        if length != 0:
            self.move_direction = (dx / length, dy / length)
        else:
            self.move_direction = (0, 0)

    def update(self, dt: float) -> None:
        x, y = self.game_object.transform.get_local_position()

        # Move along the direction vector
        new_x = x + self.move_direction[0] * self.speed * dt
        new_y = y + self.move_direction[1] * self.speed * dt

        self.game_object.transform.set_local_position(new_x, new_y)

        self.timer += dt

        if self.timer >= self.lifetime:
            self.timer = 0.0
            self.game_object.destroy()

    def on_trigger_enter(self, other):
        player_candy = other.game_object.get_component("PlayerCandy")
        if player_candy:
            player_candy.take_candy()
        self.game_object.destroy()