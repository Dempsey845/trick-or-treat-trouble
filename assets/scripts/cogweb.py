from cogworks.components.script_component import ScriptComponent
from cogworks.components.sprite import Sprite
from cogworks.components.trigger_collider import TriggerCollider


class Cobweb(ScriptComponent):
    def __init__(self):
        super().__init__()
        self.move_speed_multiplier = 0.3

    def start(self):
        sprite = Sprite("images/cobweb.png")
        self.game_object.add_component(sprite)

        trigger_collider = TriggerCollider(layer="Cobweb", layer_mask=["Player"])
        self.game_object.add_component(trigger_collider)

    def on_trigger_enter(self, other):
        other.game_object.get_component("PlayerMovement").move_speed_multiplier = self.move_speed_multiplier

    def on_trigger_exit(self, other):
        other.game_object.get_component("PlayerMovement").move_speed_multiplier = 1