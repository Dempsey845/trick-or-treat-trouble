import weakref

import pygame

from cogworks.components.script_component import ScriptComponent
from cogworks.pygame_wrappers.input_manager import InputManager


class PlayerCandy(ScriptComponent):
    def __init__(self, candy_label):
        super().__init__()
        self.candy = 5
        self.candy_label_ref = weakref.ref(candy_label)

    def start(self) -> None:
        self.candy = 5
        self.update_text()

    def update(self, dt: float) -> None:
        if InputManager.get_instance().is_key_down(pygame.K_r):
            self.game_object.scene.restart()

    def add_candy(self):
        self.candy += 1

        self.update_text()

    def update_text(self):
        candy_label = self.candy_label_ref()
        if candy_label:
            candy_label.set_text(f"Candy: {self.candy}")