import random

from cogworks import GameObject
from cogworks.components.script_component import ScriptComponent
from cogworks.components.sprite import Sprite
from cogworks.components.trigger_collider import TriggerCollider

from assets.scripts.ghost import Ghost
from assets.scripts.player_candy import PlayerCandy


class Candy(ScriptComponent):
    def __init__(self):
        super().__init__()

    def start(self) -> None:
        self.game_object.add_component(Sprite("images/circle.png"))
        self.game_object.add_component(TriggerCollider(debug=False, layer_mask=["Player"], layer="Candy"))

    def spawn_ghost(self):
        x,y = self.game_object.transform.get_world_position()
        ghost = GameObject("Ghost", x=x, y=y, scale_x=3, scale_y=3)
        ghost.add_component(Ghost(home_position=(x, y)))
        self.game_object.scene.instantiate_game_object(ghost)

    def on_trigger_enter(self, other):
        spawn_ghost = random.randint(0, 2) == 0
        if spawn_ghost:
            self.spawn_ghost()
        else:
            other.game_object.get_component(PlayerCandy).add_candy()
        self.game_object.destroy()