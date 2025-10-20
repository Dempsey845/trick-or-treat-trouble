from cogworks.components.audio_source import AudioSource
from cogworks.components.sprite import Sprite
from cogworks.components.sprite_animation import SpriteAnimation
from assets.scripts.chasing_enemy import ChasingEnemy
from assets.scripts.level_manager import LevelManager
from assets.scripts.player_candy import PlayerCandy


class AngryMan(ChasingEnemy):
    def __init__(self, home_position, move_speed=180, attack_distance=55, attack_rate=1,
                 attack_max=2, attack_time=7.0):
        super().__init__(home_position, move_speed, attack_distance, attack_rate, attack_max, attack_time)
        self.sprite = None
        self.sprite_animation = None
        self.last_dir = "side"
        self.current_animation = None
        self.last_position = None

    def start(self):
        # Attack cooldown
        self.start_attack_cooldown(1.5)

        # Sprite setup
        self.sprite = Sprite("images/man/side/man_walk1.png", pixel_art_mode=True, alpha=255)
        self.game_object.add_component(self.sprite)

        # Animation setup (using new Cogworks animation system)
        self.sprite_animation = SpriteAnimation()
        self.sprite_animation.add_animation("walk_side", "images/man/side/man_walk.png", 1, 8, 0.1)
        self.sprite_animation.add_animation("walk_down", "images/man/down/man_walk.png", 9, 16, 0.1)
        self.sprite_animation.add_animation("walk_up", "images/man/up/man_walk.png", 17, 24, 0.1)

        self.sprite_animation.set_animation("walk_side")
        self.current_animation = "walk_side"
        self.game_object.add_component(self.sprite_animation)

        # Sound setup
        ghost_sound = AudioSource("sounds/ghost.mp3", loop=True, volume=0.3, max_distance=500)
        ghost_sound.play()
        self.game_object.add_component(ghost_sound)

        # Attack counter
        self.attack_count = 1

        # Initial position
        self.last_position = self.game_object.transform.get_world_position()

    def update(self, dt):
        # Run chasing logic
        super().update(dt)

        # Compute velocity from position delta
        current_pos = self.game_object.transform.get_world_position()
        vx = current_pos[0] - self.last_position[0]
        vy = current_pos[1] - self.last_position[1]
        self.last_position = current_pos

        # Determine animation direction
        if abs(vx) > abs(vy):
            new_anim = "walk_side"
        elif vy < 0:
            new_anim = "walk_up"
        else:
            new_anim = "walk_down"

        # Only change animation if it’s different from the current one
        if new_anim != self.current_animation:
            self.sprite_animation.set_animation(new_anim)
            self.current_animation = new_anim

        # Flip sprite horizontally if moving left
        self.sprite.flip_x = vx < 0

    def perform_attack(self):
        if not self.can_attack or self.attack_count >= self.attack_max:
            return

        player = LevelManager.get_instance().get_player()
        if player:
            candy = player.get_component(PlayerCandy)
            if candy:
                candy.take_candy(10)

        # Reset attack timing
        self.attack_count += 1
        self.can_attack = False
        self.cooldown_timer = self.attack_rate
