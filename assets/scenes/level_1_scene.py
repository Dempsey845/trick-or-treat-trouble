from cogworks import GameObject
from cogworks.pygame_wrappers.window import Window

from assets.scripts.house import House
from assets.scripts.player import Player


def setup_level_1_scene(engine):
    level_1_scene = engine.create_scene("Level 1", (0, 0))

    window_width, window_height = Window.get_instance().get_size()

    player_ob = GameObject("Player", z_index=1,  x=window_width/2, y=window_height/2, scale_x=2, scale_y=2)
    player_ob.add_component(Player())

    house_ob = GameObject("House")
    house_ob.add_component(House())

    level_1_scene.add_game_object(player_ob)
    level_1_scene.add_game_object(house_ob)

    return level_1_scene