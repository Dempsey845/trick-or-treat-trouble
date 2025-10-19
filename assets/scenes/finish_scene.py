from cogworks.components.ui.ui_button import UIButton
from cogworks.components.ui.ui_image import UIImage
from cogworks.components.ui.ui_label import UILabel
from cogworks.components.ui.ui_layout import UILayout
from cogworks.components.ui.ui_transform import UITransform
from cogworks.game_object import GameObject

from assets.scripts.candy_collected_label import CandyCollectedLabel
from assets.scripts.level_manager import LevelManager


def setup_finish_scene(engine):
    menu_scene = engine.create_scene("Finish")

    def start_level(go):
        engine.set_active_scene("Level 1")

    def go_to_menu(go):
        engine.set_active_scene("Menu")

    # Create a layout
    layout = GameObject("Finish Layout")
    layout.add_component(UITransform(x=0.5, y=0.6, width=1, height=1, anchor="center"))
    layout.add_component(UILayout(vertical=True, spacing=40))
    menu_scene.add_game_object(layout)

    logo = GameObject("Logo Image")
    logo.add_component(UITransform(width=0.5, height=0.2, debug=False))
    logo.add_component(UIImage("images/tot_logo_large.png"))
    layout.add_child(logo)

    label = GameObject("Candy Label")
    label.add_component(UITransform(width=0.25, height=0.1))
    label.add_component(UILabel(f"You collected candy!", font_size=35))
    label.add_component(CandyCollectedLabel())
    layout.add_child(label)

    play_btn = GameObject("Play Button")
    play_btn.add_component(UITransform(width=0.25, height=0.1))
    play_btn.add_component(UIButton("Restart", font_size=40, on_click=start_level, border_radius=20))
    layout.add_child(play_btn)

    menu_btn = GameObject("Menu Button")
    menu_btn.add_component(UITransform(width=0.25, height=0.1))
    menu_btn.add_component(UIButton("Menu", font_size=40, on_click=go_to_menu, border_radius=20))
    layout.add_child(menu_btn)

    return menu_scene
