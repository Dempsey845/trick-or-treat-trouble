import pygame
from cogworks.components.audio_source import AudioSource
from cogworks.components.script_component import ScriptComponent


class AudioClip(ScriptComponent):
    """
    A simple scripted audio clip component that plays an audio file
    for a fixed duration, with optional fade-out and automatic cleanup.

    Ideal for one-shot sound effects or timed ambient sounds.
    """

    def __init__(self, duration: float, audio_clip_path: str, volume: float = 1.0, fade_out: bool = False):
        """
        Args:
            duration (float): Duration (in seconds) before the clip stops.
            audio_clip_path (str): Path to the audio file.
            volume (float): Playback volume (0.0–1.0).
            fade_out (bool): Whether to fade out smoothly at the end.
        """
        super().__init__()
        self.duration = duration
        self.audio_clip_path = audio_clip_path
        self.volume = volume
        self.fade_out = fade_out
        self.audio_source = None
        self._elapsed_time = 0.0
        self._is_playing = False

    def start(self) -> None:
        self.audio_source = AudioSource(clip_path=self.audio_clip_path, volume=self.volume)
        self.game_object.add_component(self.audio_source)
        self.audio_source.play()
        self._is_playing = True
        self._elapsed_time = 0.0

    def update(self, dt: float) -> None:
        if not self._is_playing or not self.audio_source:
            return

        self._elapsed_time += dt

        if self._elapsed_time >= self.duration:
            if self.fade_out:
                # Fade out smoothly over 0.5 seconds, then destroy the GameObject
                fade_ms = 500
                try:
                    sound = pygame.mixer.Sound(self.audio_source.clip_path)
                    sound.fadeout(fade_ms)
                except Exception:
                    # If fadeout fails, stop immediately
                    self.audio_source.stop()
            else:
                self.audio_source.stop()

            self._is_playing = False
            self.game_object.destroy()

    def on_destroy(self) -> None:
        if self.audio_source:
            self.audio_source.stop()
            self.audio_source = None
