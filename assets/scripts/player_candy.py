import weakref

import pygame
from cogworks import GameObject

from assets.scripts.audio_clip import AudioClip
from cogworks.components.script_component import ScriptComponent
from cogworks.pygame_wrappers.input_manager import InputManager

from assets.scripts.level_manager import LevelManager


class PlayerCandy(ScriptComponent):
    def __init__(self, candy_label):
        super().__init__()
        self.candy = 0
        self.candy_label_ref = weakref.ref(candy_label)

    def start(self) -> None:
        self.candy = 0
        LevelManager.candy_collected = 0
        self.update_text()

    def update(self, dt: float) -> None:
        if InputManager.get_instance().is_key_down(pygame.K_r):
            self.game_object.scene.restart()

    def add_candy(self, amount=1):
        self.candy += amount
        LevelManager.candy_collected = self.candy
        self.update_text()

    def take_candy(self, amount=1):
        self.candy -= amount
        if self.candy < 0:
            self.candy = 0
        LevelManager.candy_collected = self.candy
        self.spawn_audio_clip("sounds/hit.wav", 0.5, 0.5)
        self.update_text()

    def spawn_audio_clip(self, clip_path: str, duration: float, volume:float=1):
        x, y = self.game_object.transform.get_world_position()
        audio_clip = GameObject("Audio Clip", x=x, y=y)
        audio_clip.add_component(AudioClip(duration=duration, audio_clip_path=clip_path, fade_out=True, volume=volume))
        self.game_object.scene.instantiate_game_object(audio_clip)

    def update_text(self):
        candy_label = self.candy_label_ref()
        if candy_label:
            candy_label.set_text(f"Candy: {self.candy}")