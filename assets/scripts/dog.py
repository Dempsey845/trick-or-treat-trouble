from cogworks.components.audio_source import AudioSource
from cogworks.components.sprite import Sprite
from cogworks.components.sprite_animation import SpriteAnimation
from assets.scripts.chasing_enemy import ChasingEnemy
from assets.scripts.level_manager import LevelManager
from assets.scripts.player_candy import PlayerCandy

class Dog(ChasingEnemy):
    def start(self):
        self.start_attack_cooldown()
        self.sprite = Sprite("images/dog/dog1.png", pixel_art_mode=True)
        self.game_object.add_component(self.sprite)

        audio_source = AudioSource("sounds/dog_growling.mp3", loop=True, volume=0.5, max_distance=700)
        audio_source.play()
        self.game_object.add_component(audio_source)

        self._setup_animation()

    def _setup_animation(self):
        anim = SpriteAnimation()
        anim.add_animation(
            name="Run",
            sprite_path="images/dog/dog.png",
            start_sprite_index=1,
            last_sprite_index=5,
            time_between_sprites=0.1
        )
        self.game_object.add_component(anim)
        anim.set_animation("Run")

    def perform_attack(self):
        if not self.can_attack or self.attack_count >= self.attack_max:
            return
        player = LevelManager.get_instance().get_player()
        if player:
            candy_comp = player.get_component(PlayerCandy)
            if candy_comp:
                candy_comp.take_candy(1)
                if candy_comp.candy == 0:
                    self.attack_count = self.attack_max
        self.attack_count += 1
        self.cooldown_timer = self.attack_rate
        self.can_attack = False
