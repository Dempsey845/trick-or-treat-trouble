from cogworks.components.script_component import ScriptComponent
from cogworks.components.sprite import Sprite
from cogworks.components.trigger_collider import TriggerCollider

from assets.scripts.player_candy import PlayerCandy


class Candy(ScriptComponent):
    def __init__(self):
        super().__init__()

    def start(self) -> None:
        self.game_object.add_component(Sprite("images/circle.png"))
        self.game_object.add_component(TriggerCollider(debug=False, layer_mask=["Player"], layer="Candy"))

    def on_trigger_enter(self, other):
        other.game_object.get_component(PlayerCandy).add_candy()
        self.game_object.destroy()