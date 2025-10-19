from assets.scripts.audio_clip import AudioClip
from cogworks import GameObject
from cogworks.components.script_component import ScriptComponent
from cogworks.components.sprite import Sprite

from assets.scripts.level_manager import LevelManager

import math

from assets.scripts.stick import Stick


class Scarecrow(ScriptComponent):
    def __init__(self):
        super().__init__()
        self.lm = None
        self.distance_check_rate = 3
        self.timer = 0.0
        self.attack_distance = 200

    def start(self) -> None:
        self.lm = LevelManager.get_instance()

        self.game_object.add_component(Sprite("images/scarecrow.png", pixel_art_mode=True, scale_factor=4))

    def update(self, dt: float) -> None:
        self.timer += dt

        if self.timer >= self.distance_check_rate:
            self.timer = 0.0

            player_x, player_y = self.lm.get_player_position()
            x, y = self.game_object.transform.get_local_position()

            dx = x - player_x
            dy = y - player_y
            distance = math.sqrt(dx ** 2 + dy ** 2)

            if distance <= self.attack_distance:
                self.attack(player_x, player_y, distance)

    def attack(self, player_x, player_y, distance):
        x, y = self.game_object.transform.get_local_position()
        speed = distance + 50
        stick = GameObject("Stick", x=x, y=y, scale_x=1.5, scale_y=1.5)
        stick.add_component(Stick(player_x, player_y, speed))
        self.game_object.scene.instantiate_game_object(stick)
        self.spawn_audio_clip()

    def spawn_audio_clip(self):
        x, y = self.game_object.transform.get_world_position()
        audio_clip = GameObject("Audio Clip", x=x, y=y)
        audio_clip.add_component(AudioClip(duration=1, audio_clip_path="sounds/shoot.wav", fade_out=True))
        self.game_object.scene.instantiate_game_object(audio_clip)