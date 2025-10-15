from cogworks import GameObject
from cogworks.components.rigidbody2d import Rigidbody2D
from cogworks.components.sprite import Sprite
from cogworks.components.trigger_collider import TriggerCollider
from cogworks.components.ui.ui_label import UILabel
from cogworks.components.ui.ui_transform import UITransform
from cogworks.pygame_wrappers.window import Window

from assets.scripts.candy import Candy
from assets.scripts.dog import Dog
from assets.scripts.house import House
from assets.scripts.player_animation_controller import PlayerAnimationController
from assets.scripts.player_candy import PlayerCandy
from assets.scripts.player_movement import PlayerMovement


def setup_level_1_scene(engine):
    level_1_scene = engine.create_scene("Level 1", (0, 0))

    window_width, window_height = Window.get_instance().get_size()

    player_ob = GameObject("Player", z_index=1,  x=window_width/2, y=window_height/2, scale_x=2, scale_y=2)

    player_sprite = Sprite(image_path="images/player/idle/side/idle1.png", pixel_art_mode=True, scale_factor=2)
    player_ob.add_component(player_sprite)

    player_body = Rigidbody2D(debug=False, velocity_controlled=True, movement_mode="top_down", freeze_rotation=True)
    player_ob.add_component(player_body)

    player_movement = PlayerMovement()
    player_ob.add_component(player_movement)

    player_animation_controller = PlayerAnimationController()
    player_ob.add_component(player_animation_controller)

    player_trigger_collider = TriggerCollider(debug=False, layer_mask=["Candy", "House"], layer="Player")
    player_ob.add_component(player_trigger_collider)

    candy_label_ob = GameObject("Candy Label")
    candy_label_ob.add_component(UITransform(relative=True, width=0.1, height=0.1, y=0, x=0, anchor="topleft"))
    candy_label = UILabel("Candy: ")
    candy_label_ob.add_component(candy_label)
    level_1_scene.add_game_object(candy_label_ob)

    player_candy = PlayerCandy(candy_label)
    player_ob.add_component(player_candy)

    house_ob = GameObject("House")
    house_ob.add_component(House())

    dog = GameObject("Dog")
    dog.add_component(Dog(player_ob.transform))

    level_1_scene.add_game_object(player_ob)
    level_1_scene.add_game_object(house_ob)
    level_1_scene.add_game_object(dog)

    return level_1_scene