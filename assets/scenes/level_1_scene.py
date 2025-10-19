from assets.scripts.time_to_finish import TimeToFinish
from cogworks.components.ui.ui_label import UILabel

from assets.scripts.background_music import BackgroundMusic
from assets.scripts.level_manager import LevelManager

from cogworks import GameObject
from cogworks.components.sprite import Sprite
from cogworks.components.ui.ui_button import UIButton
from cogworks.components.ui.ui_transform import UITransform
from cogworks.pygame_wrappers.window import Window

from assets.scripts.camera_controller import CameraController
from assets.scripts.house import House
from assets.scripts.level_timer import LevelTimer
from assets.scripts.player import Player
from assets.scripts.road_manager import RoadManager


def add_tiles(scene, y_range, x_range, image_path, z_index, skip_x_range=None):
    for y in y_range:
        for x in x_range:
            if skip_x_range and skip_x_range[0] < x < skip_x_range[1]:
                continue
            tile_type = image_path.split("/")[-1].split(".")[0].capitalize()
            tile = GameObject(f"{tile_type}{x}{y}", x=32 * x, y=32 * y, scale_x=2, scale_y=2, z_index=z_index)
            tile.add_component(Sprite(image_path, pixel_art_mode=True))
            scene.add_game_object(tile)

def setup_level_1_scene(engine):
    level_1_scene = engine.create_scene("Level 1", (0, 0))

    level_width, level_height = (1920, 1080)
    window_width, window_height = Window.get_instance().get_size()

    background = GameObject("Background", z_index=-50, x=level_width/2, y=level_height/2)
    background.add_component(Sprite(image_path="images/background.png"))

    player_ob = GameObject("Player", z_index=1,  x=level_width/2, y=level_height/2, scale_x=2, scale_y=2)
    player_ob.add_component(Player())

    music = GameObject("Music")
    music.add_component(BackgroundMusic())
    level_1_scene.add_game_object(music)


    def exit_level(go):
        engine.set_active_scene("Menu")

    exit_btn = GameObject("Exit Button", z_index=50)
    exit_btn.add_component(UITransform(relative=True, x=0.9, y=0.02, width=0.03, height=0.03))
    exit_btn.add_component(UIButton("X", font_size=20, font_path="fonts/rainyhearts.ttf", bg_color=(255, 0, 0), on_click=exit_level, border_radius=10))
    level_1_scene.add_game_object(exit_btn)

    house_width = 32
    house_height = 32
    house_scale = 6
    house_gap = 50

    x, y = (0, 0)
    for i in range(8):
        house_x = x + 100 + (house_width * house_scale + house_gap) * i
        house_ob = GameObject("House", x=house_x, y=y)
        house_ob.add_component(House(house_width=house_width, house_height=house_height, house_scale=house_scale))
        level_1_scene.add_game_object(house_ob)

    x, y = (0, 1080//3)
    house_gap = 50
    for i in range(8):
        if i == 3 or i == 4:
            continue
        house_x = x + 100 + (house_width * house_scale + house_gap) * i
        house_ob = GameObject("House", x=house_x, y=y - (house_height * house_scale) + 270)
        house_ob.add_component(House(house_width=house_width, house_height=house_height, house_scale=house_scale))
        level_1_scene.add_game_object(house_ob)

    x, y = (0, 1080//1.5)
    house_gap = 50
    for i in range(8):
        if i == 3 or i == 4:
            continue
        house_x = x + 100 + (house_width * house_scale + house_gap) * i
        house_ob = GameObject("House", x=house_x, y=y - (house_height * house_scale) + 300)
        house_ob.add_component(House(house_width=house_width, house_height=house_height, house_scale=house_scale, spawn_bottom_webs=False))
        level_1_scene.add_game_object(house_ob)

    LAYERS = [
        # Early ground layers
        (range(0, 6), "images/grass.png", -3, None),
        (range(6, 8), "images/stone.png", -2, None),
        # Middle and upper layers (with central gap)
        (range(15, 20), "images/grass.png", -3, (21, 38)),
        (range(20, 22), "images/stone.png", -2, (21, 38)),
        (range(28, 32), "images/grass.png", -3, (21, 38)),
        (range(32, 34), "images/stone.png", -2, (21, 38)),
    ]

    for y_range, image, z, skip_range in LAYERS:
        add_tiles(level_1_scene, y_range, range(61), image, z, skip_x_range=skip_range)

    road_manager = GameObject("Road Manager")
    road_manager.add_component(RoadManager())

    camera_controlled_ob = GameObject("Camera Controller")
    max_x = 1920 - window_width//2
    max_y = 1080 - window_height//2
    camera_controlled_ob.add_component(CameraController(target_object=player_ob, max_y=max_y, min_y=window_height//2, max_x=max_x, min_x=window_width//2))

    time_label = GameObject("Time2Finish Label", z_index=50)
    time_label.add_component(UITransform(
        anchor="center", relative=True, x=0.5, y=0.05, width=0.15, height=0.05, debug=False
    ))
    time_label.add_component(UILabel("Time To Finish: 9:00 PM", font_path="fonts/rainyhearts.ttf"))
    time_label.add_component(TimeToFinish())


    level_timer_ob = GameObject("Level Timer", z_index=50)
    level_timer_ob.add_component(LevelTimer())

    level_1_scene.add_game_object(player_ob)
    level_1_scene.add_game_object(background)
    level_1_scene.add_game_object(road_manager)
    level_1_scene.add_game_object(camera_controlled_ob)
    level_1_scene.add_game_object(level_timer_ob)
    level_1_scene.add_game_object(time_label)

    return level_1_scene