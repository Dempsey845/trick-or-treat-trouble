from cogworks import GameObject
from cogworks.components.rigidbody2d import Rigidbody2D
from cogworks.components.script_component import ScriptComponent
from cogworks.components.sprite import Sprite
from cogworks.components.trigger_collider import TriggerCollider
from cogworks.components.ui.ui_label import UILabel
from cogworks.components.ui.ui_transform import UITransform

from assets.scripts.level_manager import LevelManager
from assets.scripts.player_animation_controller import PlayerAnimationController
from assets.scripts.player_candy import PlayerCandy
from assets.scripts.player_movement import PlayerMovement


class Player(ScriptComponent):

    def __init__(self):
        super().__init__()

    def start(self) -> None:
        lm = LevelManager.get_instance()
        lm.register_player(self.game_object)

        candy_label_ob = GameObject("Candy Label")
        candy_label_ob.add_component(UITransform(relative=True, width=0.1, height=0.1, y=0, x=0, anchor="topleft"))
        candy_label = UILabel("Candy: ")
        candy_label_ob.add_component(candy_label)

        self.game_object.scene.instantiate_game_object(candy_label_ob)

        player_sprite = Sprite(image_path="images/player/idle/side/idle1.png", pixel_art_mode=True, scale_factor=2)
        self.game_object.add_component(player_sprite)

        player_body = Rigidbody2D(debug=False, velocity_controlled=True, movement_mode="top_down", freeze_rotation=True)
        self.game_object.add_component(player_body)

        player_movement = PlayerMovement()
        self.game_object.add_component(player_movement)

        player_animation_controller = PlayerAnimationController()
        self.game_object.add_component(player_animation_controller)

        player_trigger_collider = TriggerCollider(debug=False, layer_mask=["Candy", "House"], layer="Player")
        self.game_object.add_component(player_trigger_collider)

        player_candy = PlayerCandy(candy_label)
        self.game_object.add_component(player_candy)