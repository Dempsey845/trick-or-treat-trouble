import weakref

import pygame

from assets.scripts.angry_man import AngryMan
from cogworks.pygame_wrappers.input_manager import InputManager

from assets.scripts.interact_prompt import InteractPrompt
from cogworks import GameObject

from cogworks.components.trigger_collider import TriggerCollider

from cogworks.components.sprite import Sprite

from cogworks.components.script_component import ScriptComponent


class CandyBucket(ScriptComponent):
    candy_amount = 10
    def __init__(self):
        super().__init__()
        self.player_ref = None
        self.prompt_ref = None
        self.input = None

    def start(self) -> None:
        self.game_object.add_component(Sprite(image_path="images/candy_bucket.png", pixel_art_mode=True))
        self.game_object.add_component(TriggerCollider(layer="Candy Bucket", layer_mask=["Player"], debug=False))
        self.input = InputManager.get_instance()

    def on_trigger_stay(self, other):
        if not self.input:
            return

        if self.input.is_key_down(pygame.K_e):
            player = self.player_ref()
            if player:
                player.get_component("PlayerCandy").add_candy(self.candy_amount)

            x, y = self.game_object.transform.get_local_position()
            man = GameObject("AngryMan", x=x, y=y, scale_x=2, scale_y=2)
            man.add_component(AngryMan(home_position=(x, y)))
            self.game_object.scene.instantiate_game_object(man)

            prompt = self.prompt_ref()
            if prompt:
                prompt.destroy()

            self.game_object.destroy()

    def on_trigger_enter(self, other):
        self.player_ref = weakref.ref(other.game_object)

        prompt = GameObject("Prompt", z_index=50)
        x, y = self.game_object.transform.get_world_position()
        bucket_height = self.game_object.get_component(TriggerCollider).height
        print(bucket_height)
        prompt.add_component(InteractPrompt(x, y + (bucket_height // 2) - 25))

        self.game_object.scene.instantiate_game_object(prompt)

        self.prompt_ref = weakref.ref(prompt)

    def on_trigger_exit(self, other):
        prompt = self.prompt_ref()
        if prompt:
            prompt.destroy()
