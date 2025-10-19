from assets.scripts.background_music import BackgroundMusic
from cogworks.components.audio_source import AudioSource

from cogworks.components.background import Background

from cogworks.components.sprite import Sprite

from cogworks import GameObject
from cogworks.components.ui.ui_button import UIButton
from cogworks.components.ui.ui_label import UILabel
from cogworks.components.ui.ui_transform import UITransform

from assets.scripts.intro_label import IntroLabel


def setup_introduction_scene(engine):
    scene = engine.create_scene("Introduction")

    def exit_level(go):
        engine.set_active_scene("Menu")

    exit_btn = GameObject("Exit Button", z_index=50)
    exit_btn.add_component(UITransform(relative=True, x=0.9, y=0.02, width=0.03, height=0.03))
    exit_btn.add_component(UIButton("X", font_size=20, bg_color=(255, 0, 0), on_click=exit_level, border_radius=10))
    scene.add_game_object(exit_btn)

    intro_label = GameObject("Introduction Label")
    intro_label.add_component(UITransform(relative=True, x=0.5, y=0.5, width=0.5, height=0.1, anchor="center"))
    intro_label.add_component(UILabel("You have until", font_size=40, font_path="fonts/rainyhearts.ttf"))
    intro_label.add_component(IntroLabel())

    background_music = GameObject("Background Music")
    background_music.add_component(BackgroundMusic("sounds/music.mp3"))
    scene.add_game_object(background_music)

    background = GameObject("Background", z_index=-1)
    background.add_component(Sprite("images/introduction_background.png"))
    background.add_component(Background())
    scene.add_game_object(background)

    scene.add_game_object(intro_label)