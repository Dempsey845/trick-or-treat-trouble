from cogworks import GameObject
from cogworks.components.sprite import Sprite
from cogworks.pygame_wrappers.window import Window

from assets.scripts.camera_controller import CameraController
from assets.scripts.house import House
from assets.scripts.level_timer import LevelTimer
from assets.scripts.player import Player
from assets.scripts.road_manager import RoadManager
from assets.scripts.witch_head import WitchHead


def setup_level_1_scene(engine):
    level_1_scene = engine.create_scene("Level 1", (0, 0))

    level_width, level_height = (1920, 1080)
    window_width, window_height = Window.get_instance().get_size()

    background = GameObject("Background", z_index=-50, x=level_width/2, y=level_height/2)
    background.add_component(Sprite(image_path="images/background.png"))


    player_ob = GameObject("Player", z_index=1,  x=level_width/2, y=level_height/2, scale_x=2, scale_y=2)
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
        house_ob = GameObject("House", x=house_x, y=y - (house_height * house_scale) + 270)
        house_ob.add_component(House(house_width=house_width, house_height=house_height, house_scale=house_scale))
        level_1_scene.add_game_object(house_ob)

    x, y = level_1_scene.camera_component.get_world_position_of_point("bottomleft")
    house_gap = 50
    for i in range(8):
        if i == 3 or i == 4:
            continue
        house_x = x + 100 + (house_width * house_scale + house_gap) * i
        house_ob = GameObject("House", x=house_x, y=y - (house_height * house_scale) + 300)
        house_ob.add_component(House(house_width=house_width, house_height=house_height, house_scale=house_scale))
        level_1_scene.add_game_object(house_ob)

    for y in range(6):
        for x in range(61):
            grass_ob = GameObject(f"Grass{x}{y}", x=32*x, y=32*y, scale_x=2, scale_y=2, z_index=-3)
            grass_ob.add_component(Sprite("images/grass.png", pixel_art_mode=True))
            level_1_scene.add_game_object(grass_ob)

    for y in range(6, 8):
        for x in range(61):
            stone_ob = GameObject(f"Stone{x}{y}", x=32*x, y=32*y, scale_x=2, scale_y=2, z_index=-2)
            stone_ob.add_component(Sprite("images/stone.png", pixel_art_mode=True))
            level_1_scene.add_game_object(stone_ob)

    for y in range(15, 20):
        for x in range(61):
            if 21 < x < 38:
                continue
            grass_ob = GameObject(f"Grass{x}{y}", x=32*x, y=32*y, scale_x=2, scale_y=2, z_index=-3)
            grass_ob.add_component(Sprite("images/grass.png", pixel_art_mode=True))
            level_1_scene.add_game_object(grass_ob)

    for y in range(20, 22):
        for x in range(61):
            if 21 < x < 38:
                continue
            stone_ob = GameObject(f"Stone{x}{y}", x=32*x, y=32*y, scale_x=2, scale_y=2, z_index=-2)
            stone_ob.add_component(Sprite("images/stone.png", pixel_art_mode=True))
            level_1_scene.add_game_object(stone_ob)

    for y in range(28, 32):
        for x in range(61):
            if 21 < x < 38:
                continue
            grass_ob = GameObject(f"Grass{x}{y}", x=32*x, y=32*y, scale_x=2, scale_y=2, z_index=-3)
            grass_ob.add_component(Sprite("images/grass.png", pixel_art_mode=True))
            level_1_scene.add_game_object(grass_ob)

    for y in range(32, 34):
        for x in range(61):
            if 21 < x < 38:
                continue
            stone_ob = GameObject(f"Stone{x}{y}", x=32 * x, y=32 * y, scale_x=2, scale_y=2, z_index=-2)
            stone_ob.add_component(Sprite("images/stone.png", pixel_art_mode=True))
            level_1_scene.add_game_object(stone_ob)

    road_manager = GameObject("Road Manager")
    road_manager.add_component(RoadManager())

    camera_controlled_ob = GameObject("Camera Controller")
    max_x = 1920 - window_width//2
    max_y = 1080 - window_height//2
    camera_controlled_ob.add_component(CameraController(target_object=player_ob, max_y=max_y, min_y=window_height//2, max_x=max_x, min_x=window_width//2))

    level_timer_ob = GameObject("Level Timer", z_index=50)
    level_timer_ob.add_component(LevelTimer())

    level_1_scene.add_game_object(player_ob)
    level_1_scene.add_game_object(background)
    level_1_scene.add_game_object(road_manager)
    level_1_scene.add_game_object(camera_controlled_ob)
    level_1_scene.add_game_object(level_timer_ob)

    return level_1_scene