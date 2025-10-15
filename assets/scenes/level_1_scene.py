from cogworks import GameObject
from cogworks.components.sprite import Sprite
from cogworks.pygame_wrappers.window import Window

from assets.scripts.house import House
from assets.scripts.player import Player


def setup_level_1_scene(engine):
    level_1_scene = engine.create_scene("Level 1", (0, 0))

    window_width, window_height = Window.get_instance().get_size()

    background = GameObject("Background", z_index=-50, x=window_width/2, y=window_height/2)
    background.add_component(Sprite(image_path="images/background.png"))


    player_ob = GameObject("Player", z_index=1,  x=window_width/2, y=window_height/2, scale_x=2, scale_y=2)
    player_ob.add_component(Player())

    house_width = 32
    house_height = 32
    house_scale = 6
    house_gap = 50

    x, y = level_1_scene.camera_component.get_world_position_of_point("topleft")
    for i in range(8):
        house_x = x + 100 + (house_width * house_scale + house_gap) * i
        house_ob = GameObject("House", x=house_x, y=y)
        house_ob.add_component(House(house_width=house_width, house_height=house_height, house_scale=house_scale))
        level_1_scene.add_game_object(house_ob)

    x, y = level_1_scene.camera_component.get_world_position_of_point("leftcenter")
    house_gap = 50
    for i in range(8):
        if i == 3 or i == 4:
            continue
        house_x = x + 100 + (house_width * house_scale + house_gap) * i
        house_ob = GameObject("House", x=house_x, y=y - (house_height * house_scale) + 100)
        house_ob.add_component(House(house_width=house_width, house_height=house_height, house_scale=house_scale))
        level_1_scene.add_game_object(house_ob)

    x, y = level_1_scene.camera_component.get_world_position_of_point("bottomleft")
    house_gap = 50
    for i in range(8):
        if i == 3 or i == 4:
            continue
        house_x = x + 100 + (house_width * house_scale + house_gap) * i
        house_ob = GameObject("House", x=house_x, y=y - (house_height * house_scale) - 50)
        house_ob.add_component(House(house_width=house_width, house_height=house_height, house_scale=house_scale))
        level_1_scene.add_game_object(house_ob)

    level_1_scene.add_game_object(player_ob)
    level_1_scene.add_game_object(background)

    return level_1_scene