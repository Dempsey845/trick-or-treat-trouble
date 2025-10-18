from cogworks.components.ui.ui_button import UIButton
from cogworks.components.ui.ui_image import UIImage
from cogworks.components.ui.ui_label import UILabel
from cogworks.components.ui.ui_layout import UILayout
from cogworks.components.ui.ui_transform import UITransform
from cogworks.game_object import GameObject


def setup_menu_scene(engine):
    menu_scene = engine.create_scene("Menu")

    def start_level(go):
        engine.set_active_scene("Level 1")

    def exit_game(go):
        engine.quit()

    # Create a layout
    layout = GameObject("Menu Layout")
    layout.add_component(UITransform(x=0.5, y=0.6, width=1, height=1, anchor="center"))
    layout.add_component(UILayout(vertical=True, spacing=40))
    menu_scene.add_game_object(layout)

    # Logo
    logo = GameObject("Logo Image")
    logo.add_component(UITransform(width=0.5, height=0.2, debug=False))
    logo.add_component(UIImage("images/tot_logo_large.png"))
    layout.add_child(logo)

    play_btn = GameObject("Play Button")
    play_btn.add_component(UITransform(width=0.25, height=0.1))
    play_btn.add_component(UIButton("Play", font_size=40, on_click=start_level, border_radius=20))
    layout.add_child(play_btn)

    exit_btn = GameObject("Exit Button")
    exit_btn.add_component(UITransform(width=0.25, height=0.1))
    exit_btn.add_component(UIButton("Exit", font_size=40, on_click=exit_game, border_radius=20))
    layout.add_child(exit_btn)

    return menu_scene
