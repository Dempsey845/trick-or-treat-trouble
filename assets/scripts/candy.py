import random

from assets.scripts.audio_clip import AudioClip
from cogworks.components.audio_source import AudioSource

from cogworks import GameObject
from cogworks.components.script_component import ScriptComponent
from cogworks.components.sprite import Sprite
from cogworks.components.trigger_collider import TriggerCollider

from assets.scripts.ghost import Ghost
from assets.scripts.player_candy import PlayerCandy


class Candy(ScriptComponent):
    def __init__(self):
        super().__init__()

    def start(self) -> None:
        self.game_object.add_component(Sprite("images/candy.png", pixel_art_mode=True))
        self.game_object.add_component(TriggerCollider(debug=False, layer_mask=["Player"], layer="Candy"))

    def spawn_ghost(self):
        x,y = self.game_object.transform.get_world_position()
        ghost = GameObject("Ghost", x=x, y=y, scale_x=3, scale_y=3)
        ghost.add_component(Ghost(home_position=(x, y)))
        self.game_object.scene.instantiate_game_object(ghost)

    def spawn_audio_clip(self):
        x, y = self.game_object.transform.get_world_position()
        audio_clip = GameObject("Audio Clip", x=x, y=y)
        audio_clip.add_component(AudioClip(duration=0.5, audio_clip_path="sounds/pickup_coin.wav", fade_out=True))
        self.game_object.scene.instantiate_game_object(audio_clip)

    def on_trigger_enter(self, other):
        player_candy = other.game_object.get_component(PlayerCandy)

        if player_candy.candy <= 0:
            player_candy.add_candy()
        else:
            spawn_ghost = random.randint(0, 2) == 0
            if spawn_ghost:
                self.spawn_ghost()
            else:
                player_candy.add_candy()

        self.spawn_audio_clip()
        self.game_object.destroy()