import random

from cogworks.components.audio_listener import AudioListener

from cogworks import GameObject
from cogworks.components.linerenderer import LineRenderer
from cogworks.components.rigidbody2d import Rigidbody2D
from cogworks.components.script_component import ScriptComponent
from cogworks.components.sprite import Sprite
from cogworks.components.trigger_collider import TriggerCollider
from cogworks.components.ui.ui_label import UILabel
from cogworks.components.ui.ui_transform import UITransform

from assets.scripts.house_manager import HouseManager
from assets.scripts.level_manager import LevelManager
from assets.scripts.player_animation_controller import PlayerAnimationController
from assets.scripts.player_candy import PlayerCandy
from assets.scripts.player_movement import PlayerMovement


class Player(ScriptComponent):

    def __init__(self):
        super().__init__()
        self.line_renderer = None

    def start(self) -> None:
        lm = LevelManager.get_instance()
        lm.register_player(self.game_object)

        candy_label_ob = GameObject("Candy Label", z_index=100)
        candy_label_ob.add_component(UITransform(relative=True, width=0.15, height=0.05, y=0.025, x=0.05, debug=False, anchor="topleft"))
        candy_label = UILabel("Candy: ", font_size=40, font_path="fonts/rainyhearts.ttf")
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

        scale = self.game_object.transform.local_scale_x
        player_trigger_collider = TriggerCollider(debug=False, width=12 * scale, height=14 * scale, layer_mask=["Candy", "House", "Cobweb", "Projectile", "Candy Bucket"], layer="Player")
        self.game_object.add_component(player_trigger_collider)

        player_candy = PlayerCandy(candy_label)
        self.game_object.add_component(player_candy)

        self.game_object.scene.camera.get_component(AudioListener).set_target_transform(self.game_object.transform)

    def add_marker(self):
        self.remove_marker()

        trick_marker = random.randint(0, 1) == 0

        point_a = self.game_object.transform.get_local_position()
        point_b = HouseManager.get_instance().get_random_treat_house_door_pos() if not trick_marker else HouseManager.get_instance().get_random_trick_house_door_pos()

        if point_b is None:
            return

        self.line_renderer = LineRenderer(point_a=point_a,
                                          point_b=point_b,
                                          style="dashed",
                                          color=(255, 255, 0), alpha=150)
        self.game_object.add_component(self.line_renderer)

    def remove_marker(self):
        if self.line_renderer:
            self.line_renderer = None
            self.game_object.remove_component(LineRenderer)

    def update(self, dt:float):
        if self.line_renderer:
            self.line_renderer.point_a=self.game_object.transform.get_local_position()

    def on_remove(self):
        lm = LevelManager.get_instance()
        lm.deregister_player()

    def on_disabled(self):
        HouseManager.get_instance().restart()
        lm = LevelManager.get_instance()
        lm.deregister_player()
