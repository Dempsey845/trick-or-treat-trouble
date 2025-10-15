import random
import weakref

import pygame
from cogworks import GameObject
from cogworks.components.rigidbody2d import Rigidbody2D
from cogworks.components.script_component import ScriptComponent
from cogworks.components.sprite import Sprite
from cogworks.components.trigger_collider import TriggerCollider
from cogworks.components.ui.ui_label import UILabel
from cogworks.components.ui.ui_transform import UITransform
from cogworks.pygame_wrappers.input_manager import InputManager

from assets.scripts.interact_prompt import InteractPrompt
from assets.scripts.level_manager import LevelManager
from assets.scripts.trick_manager import TrickManager
from assets.scripts.trick_or_treat_prompt import TrickOrTreatPrompt


class House(ScriptComponent):
    def __init__(self, house_width=32, house_height=32, house_scale=6):
        super().__init__()
        self.input = None
        self.can_knock = True
        self.house_scale = 6
        self.house_width = house_width * house_scale
        self.house_height = house_height * house_scale
        self.prompt_ref = None
        self.trick_manager = None
        self.dog_spawn_pos = (0, 0)

    def start(self) -> None:
        x, y = self.game_object.transform.get_local_position()
        house_scale = self.house_scale
        house_width = self.house_width
        house_height = self.house_height
        self.game_object.transform.set_local_scale(house_scale)
        self.game_object.transform.set_local_position(x, y + house_height//2)

        self.dog_spawn_pos = (x, y + house_height)

        sprite = Sprite(image_path="images/house_base.png", pixel_art_mode=True)
        self.game_object.add_component(sprite)

        y += self.house_height//2
        roof = GameObject("Roof", x=x, y=y, scale_x = self.house_scale, scale_y = self.house_scale, z_index=5)
        roof.add_component(Sprite(image_path="images/house_roof.png", pixel_art_mode=True))
        self.game_object.scene.instantiate_game_object(roof)

        decoration = GameObject("Decoration", x=x, y=y, scale_x=self.house_scale, scale_y=self.house_scale, z_index=5)
        decoration.add_component(Sprite(image_path="images/house_dec.png", pixel_art_mode=True))
        self.game_object.scene.instantiate_game_object(decoration)

        body = Rigidbody2D(debug=True, static=True, width=house_width-40, height=house_height - 50)
        self.game_object.add_component(body)

        trigger_collider = TriggerCollider(layer="House", width=50, height=50, offset_y=house_height//2, debug=True)
        self.game_object.add_component(trigger_collider)

        self.trick_manager = TrickManager(self)
        self.game_object.add_component(self.trick_manager)

        self.input = InputManager.get_instance()
        self.can_knock = True

    def knock(self):
        trick = random.randint(0, 1) == 0
        name = "Trick Prompt" if trick else "Treat Prompt"
        prompt = GameObject(name=name)
        prompt.add_component(TrickOrTreatPrompt(trick))
        self.game_object.scene.instantiate_game_object(prompt)

        if trick:
            self.trick_manager.perform_random_trick()
        else:
            player_candy = LevelManager.get_instance().get_player_candy()()
            if player_candy:
                player_candy.add_candy()

        prompt = self.prompt_ref()
        if prompt:
            prompt.destroy()

    def on_trigger_stay(self, other):
        if not self.input:
            return

        if self.input.is_key_down(pygame.K_e) and self.can_knock:
            self.can_knock = False
            self.knock()

    def on_trigger_enter(self, other):
        if not self.can_knock:
            return

        prompt = GameObject("Prompt", z_index=50)
        x, y = self.game_object.transform.get_world_position()
        prompt.add_component(InteractPrompt(x, y+(self.house_height//2)-25))

        self.game_object.scene.instantiate_game_object(prompt)

        self.prompt_ref = weakref.ref(prompt)

    def on_trigger_exit(self, other):
        prompt = self.prompt_ref()
        if prompt:
            prompt.destroy()
