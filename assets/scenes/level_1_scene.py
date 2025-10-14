from cogworks import GameObject
from cogworks.components.rigidbody2d import Rigidbody2D
from cogworks.components.sprite import Sprite
from cogworks.pygame_wrappers.window import Window

from assets.scripts.player_animation_controller import PlayerAnimationController
from assets.scripts.player_movement import PlayerMovement


def setup_level_1_scene(engine):
    level_1_scene = engine.create_scene("Level 1", (0, 0))

    window_width, window_height = Window.get_instance().get_size()

    player_ob = GameObject("Player", x=window_width/2, y=window_height/2, scale_x=2, scale_y=2)

    player_sprite = Sprite(image_path="images/player/idle/side/idle1.png", pixel_art_mode=True, scale_factor=2)
    player_ob.add_component(player_sprite)

    player_body = Rigidbody2D(debug=False, velocity_controlled=True, movement_mode="top_down", freeze_rotation=True)
    player_ob.add_component(player_body)

    player_movement = PlayerMovement()
    player_ob.add_component(player_movement)

    player_animation_controller = PlayerAnimationController()
    player_ob.add_component(player_animation_controller)

    wall_ob = GameObject("Wall", x=window_width - 300, y=window_height/2, scale_x=5, scale_y=5)

    wall_sprite = Sprite(image_path="images/square.png")
    wall_ob.add_component(wall_sprite)

    wall_body = Rigidbody2D(debug=True, static=True)
    wall_ob.add_component(wall_body)

    level_1_scene.add_game_object(player_ob)
    level_1_scene.add_game_object(wall_ob)

    return level_1_scene