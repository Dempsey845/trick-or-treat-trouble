from cogworks.components.audio_source import AudioSource

from cogworks.components.script_component import ScriptComponent


class BackgroundMusic(ScriptComponent):
    def __init__(self, path="sounds/background_music.mp3", volume=0.3, loop=True):
        super().__init__()
        self.path = path
        self.volume = volume
        self.loop = loop

    def start(self) -> None:
        music_audio_source = AudioSource(self.path, volume=self.volume, loop=self.loop)
        self.game_object.add_component(music_audio_source)
        music_audio_source.play(bypass_spatial=True)