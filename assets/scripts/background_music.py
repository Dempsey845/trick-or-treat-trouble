from cogworks.components.audio_source import AudioSource

from cogworks.components.script_component import ScriptComponent


class BackgroundMusic(ScriptComponent):
    def __init__(self):
        super().__init__()

    def start(self) -> None:
        music_audio_source = AudioSource("sounds/background_music.mp3", volume=0.3, loop=True)
        self.game_object.add_component(music_audio_source)
        music_audio_source.play(bypass_spatial=True)