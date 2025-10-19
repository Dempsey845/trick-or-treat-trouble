from cogworks import GameObject

from assets.scripts.audio_clip import AudioClip
from cogworks.components.script_component import ScriptComponent
from cogworks.components.sprite import Sprite


class WitchHead(ScriptComponent):
    def __init__(self):
        super().__init__()
        self.animation_time = 1.5  # total duration of the animation (fast pop)
        self.elapsed_time = 0.0
        self.start_scale = 0.1
        self.max_scale = 1.5
        self.end_scale = 0.1
        self.sprite = None
        self.phase = "scaling_up"  # animation phases: scaling_up -> scaling_down

    def spawn_audio_clip(self):
        x, y = self.game_object.transform.get_world_position()
        audio_clip = GameObject("Audio Clip", x=x, y=y)
        audio_clip.add_component(AudioClip(duration=5, audio_clip_path="sounds/witch.mp3", fade_out=True))
        self.game_object.scene.instantiate_game_object(audio_clip)

    def start(self):
        self.game_object.transform.local_scale_x = self.start_scale
        self.game_object.transform.local_scale_y = self.start_scale

        self.sprite = Sprite("images/witch_head.png", scale_factor=30, pixel_art_mode=True, alpha=150)
        self.game_object.add_component(self.sprite)

        self.spawn_audio_clip()

    def update(self, dt: float):
        self.elapsed_time += dt

        if self.phase == "scaling_up":
            t = min(self.elapsed_time / (self.animation_time / 2), 1.0)
            scale = self.start_scale + (self.max_scale - self.start_scale) * t
            self.game_object.transform.local_scale_x = scale
            self.game_object.transform.local_scale_y = scale

            if t >= 1.0:
                self.phase = "scaling_down"
                self.elapsed_time = 0.0

        elif self.phase == "scaling_down":
            t = min(self.elapsed_time / (self.animation_time / 2), 1.0)
            scale = self.max_scale + (self.end_scale - self.max_scale) * t
            self.game_object.transform.local_scale_x = scale
            self.game_object.transform.local_scale_y = scale

            if t >= 1.0:
                self.game_object.destroy()
