import random
import weakref

import pygame
from cogworks import GameObject
from cogworks.components.rigidbody2d import Rigidbody2D
from cogworks.components.script_component import ScriptComponent
from cogworks.components.sprite import Sprite
from cogworks.components.trigger_collider import TriggerCollider
from cogworks.pygame_wrappers.input_manager import InputManager

from assets.scripts.cogweb import Cobweb
from assets.scripts.interact_prompt import InteractPrompt
from assets.scripts.level_manager import LevelManager
from assets.scripts.trick_manager import TrickManager
from assets.scripts.trick_or_treat_prompt import TrickOrTreatPrompt

from assets.scripts.house_manager import HouseManager


class House(ScriptComponent):
    def __init__(self, house_width=32, house_height=32, house_scale=6):
        super().__init__()
        self.player_ref = None
        self.input = None
        self.can_knock = True
        self.house_scale = 6
        self.house_width = house_width * house_scale
        self.house_height = house_height * house_scale
        self.prompt_ref = None
        self.trick_manager = None
        self.door_pos = (0, 0)
        self.is_trick = False

    def start(self) -> None:
        x, y = self.game_object.transform.get_local_position()
        house_scale = self.house_scale
        house_width = self.house_width
        house_height = self.house_height
        self.game_object.transform.set_local_scale(house_scale)
        self.game_object.transform.set_local_position(x, y + house_height//2)

        self.door_pos = (x, y + house_height)

        sprite = Sprite(image_path="images/house_base.png", pixel_art_mode=True)
        self.game_object.add_component(sprite)

        y += self.house_height//2
        roof = GameObject("Roof", x=x, y=y, scale_x = self.house_scale, scale_y = self.house_scale, z_index=5)
        roof.add_component(Sprite(image_path="images/house_roof.png", pixel_art_mode=True))
        self.game_object.scene.instantiate_game_object(roof)

        decoration = GameObject("Decoration", x=x, y=y, scale_x=self.house_scale, scale_y=self.house_scale, z_index=5)
        random_dec = random.randint(1, 2)
        decoration.add_component(Sprite(image_path=f"images/house_dec_{random_dec}.png", pixel_art_mode=True))
        self.game_object.scene.instantiate_game_object(decoration)

        body = Rigidbody2D(debug=True, static=True, width=house_width-40, height=house_height - 50)
        self.game_object.add_component(body)

        trigger_collider = TriggerCollider(layer="House", width=50, height=50, offset_y=house_height//2, debug=True)
        self.game_object.add_component(trigger_collider)

        self.trick_manager = TrickManager(self)
        self.game_object.add_component(self.trick_manager)

        self.input = InputManager.get_instance()
        self.can_knock = True

        x, y = self.game_object.transform.get_local_position()
        web_scale = 2.5
        cobweb_1 = GameObject("Cobweb", z_index=2, x=x + self.house_width//2 + 32, y=y, scale_x=web_scale, scale_y=web_scale)
        cobweb_1.add_component(Cobweb())

        cobweb_2 = GameObject("Cobweb2", z_index=2, x=x - self.house_width//2 - 32, y=y + random.randint(0, 64), scale_x=web_scale, scale_y=web_scale)
        cobweb_2.add_component(Cobweb())

        cobweb_3 = GameObject("Cobweb3", z_index=2, x=x - 64, y=y + self.house_height//2, scale_x=web_scale, scale_y=web_scale)
        cobweb_3.add_component(Cobweb())

        cobweb_4 = GameObject("Cobweb4", z_index=2, x=x + 64, y=y + self.house_height // 2, scale_x=web_scale,
                              scale_y=web_scale)
        cobweb_4.add_component(Cobweb())

        if random.randint(0, 1) == 0:
            self.game_object.scene.instantiate_game_object(cobweb_1)
        if random.randint(0, 1) == 0:
            self.game_object.scene.instantiate_game_object(cobweb_2)
        if random.randint(0, 1) == 0:
            self.game_object.scene.instantiate_game_object(cobweb_3)
        else:
            self.game_object.scene.instantiate_game_object(cobweb_4)

        HouseManager.get_instance().register_house(self)

    def knock(self):
        is_trick = self.is_trick
        name = "Trick Prompt" if is_trick else "Treat Prompt"
        prompt = GameObject(name=name)
        prompt.add_component(TrickOrTreatPrompt(is_trick))
        self.game_object.scene.instantiate_game_object(prompt)

        player = self.player_ref()
        if player:
            player.get_component("Player").remove_marker()

        if is_trick:
            self.trick_manager.perform_random_trick()
        else:
            player_candy = LevelManager.get_instance().get_player_candy()()
            if player_candy:
                player_candy.add_candy(random.randint(1, 3))

            give_marker = random.randint(0, 1) == 0
            player = self.player_ref()

            if give_marker and player:
                player.get_component("Player").add_marker()

        prompt = self.prompt_ref()
        if prompt:
            prompt.destroy()

        self.game_object.get_component("Sprite").change_image("images/house_base_closed.png")

    def on_trigger_stay(self, other):
        if not self.input:
            return

        if self.input.is_key_down(pygame.K_e) and self.can_knock:
            self.can_knock = False
            self.knock()

    def on_trigger_enter(self, other):
        if not self.can_knock:
            return

        self.player_ref = weakref.ref(other.game_object)

        prompt = GameObject("Prompt", z_index=50)
        x, y = self.game_object.transform.get_world_position()
        prompt.add_component(InteractPrompt(x, y+(self.house_height//2)-25))

        self.game_object.scene.instantiate_game_object(prompt)

        self.prompt_ref = weakref.ref(prompt)

    def on_trigger_exit(self, other):
        prompt = self.prompt_ref()
        if prompt:
            prompt.destroy()
