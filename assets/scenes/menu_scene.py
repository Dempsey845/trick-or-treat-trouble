from assets.scripts.background_music import BackgroundMusic
from cogworks.components.background import Background
from cogworks.components.sprite import Sprite

from assets.scripts.level_manager import LevelManager
from cogworks.components.ui.ui_button import UIButton
from cogworks.components.ui.ui_image import UIImage
from cogworks.components.ui.ui_label import UILabel
from cogworks.components.ui.ui_layout import UILayout
from cogworks.components.ui.ui_transform import UITransform
from cogworks.game_object import GameObject


def setup_menu_scene(engine):
    menu_scene = engine.create_scene("Menu")

    def start_level(go):
        LevelManager.difficulty = "easy"
        engine.set_active_scene("Introduction")

    def start_hard_level(go):
        LevelManager.difficulty = "hard"
        engine.set_active_scene("Introduction")

    def exit_game(go):
        engine.quit()

    # Create a layout
    layout = GameObject("Menu Layout")
    layout.add_component(UITransform(x=0.4, y=1, width=1, height=1, anchor="center"))
    layout.add_component(UILayout(vertical=True, spacing=40))
    menu_scene.add_game_object(layout)

    play_btn = GameObject("Play Button")
    play_btn.add_component(UITransform(width=0.15, height=0.05))
    play_btn.add_component(UIButton("Play (Easy)", bg_color=(20, 20, 20), font_size=40, font_path="fonts/rainyhearts.ttf", on_click=start_level, border_radius=10))
    layout.add_child(play_btn)

    play_hard_btn = GameObject("Play Button")
    play_hard_btn.add_component(UITransform(width=0.15, height=0.05))
    play_hard_btn.add_component(UIButton("Play (Hard)", bg_color=(20, 20, 20), font_size=40, font_path="fonts/rainyhearts.ttf", on_click=start_hard_level, border_radius=10))
    layout.add_child(play_hard_btn)

    exit_btn = GameObject("Exit Button")
    exit_btn.add_component(UITransform(width=0.15, height=0.05))
    exit_btn.add_component(UIButton("Exit", bg_color=(20, 20, 20), font_size=40, font_path="fonts/rainyhearts.ttf", on_click=exit_game, border_radius=10))
    layout.add_child(exit_btn)

    background_music = GameObject("Background Music")
    background_music.add_component(BackgroundMusic("sounds/menu_music.mp3"))
    menu_scene.add_game_object(background_music)

    background = GameObject("Background", z_index=-1)
    background.add_component(Sprite("images/menu_background.png"))
    background.add_component(Background())
    menu_scene.add_game_object(background)

    return menu_scene
