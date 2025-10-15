import math
from cogworks.components.script_component import ScriptComponent
from cogworks.components.sprite import Sprite
from cogworks.components.sprite_animation import SpriteAnimation
from assets.scripts.level_manager import LevelManager


class Dog(ScriptComponent):
    def __init__(self, home_position):
        super().__init__()
        self.move_speed = 160
        self.attack_distance = 55
        self.attack_rate = 1
        self.cooldown_timer = self.attack_rate  # start on cooldown
        self.can_attack = False  # start unable to attack
        self.attack_max = 3
        self.attack_count = 0
        self.attack_time = 7.0
        self.attack_timer = 0.0
        self.home_position = home_position
        self.sprite = None

    def start(self) -> None:
        self.sprite = Sprite("images/dog/dog1.png", pixel_art_mode=True)
        self.game_object.add_component(self.sprite)
        self._setup_animation()

    def _setup_animation(self):
        sprite_animation = SpriteAnimation()
        sprite_animation.add_animation(
            name="Run",
            sprite_path="images/dog/dog.png",
            start_sprite_index=1,
            last_sprite_index=5,
            time_between_sprites=0.1
        )
        self.game_object.add_component(sprite_animation)
        sprite_animation.set_animation("Run")

    def update(self, dt: float) -> None:
        self.attack_timer += dt
        self.handle_attack_cooldown(dt)

        target_x, target_y, hover = self.get_target_position()
        dir_x, dir_y = self.calculate_movement_direction(target_x, target_y, hover)
        self.apply_movement(dir_x, dir_y, target_x, target_y, dt)

        # Destroy dog if it has returned home and stopped moving
        if not hover:
            dog_x, dog_y = self.game_object.transform.get_world_position()
            if math.hypot(target_x - dog_x, target_y - dog_y) < 5:
                self.game_object.destroy()

    # --- Attack Handling ---
    def handle_attack_cooldown(self, dt: float):
        if not self.can_attack:
            self.cooldown_timer -= dt
            if self.cooldown_timer <= 0:
                self.can_attack = True

        # Only attack if under max attacks and within attack time
        if self.attack_count >= self.attack_max or self.attack_timer >= self.attack_time:
            return

        player_pos = LevelManager.get_instance().get_player_position()
        if not player_pos:
            return

        dog_x, dog_y = self.game_object.transform.get_world_position()
        player_x, player_y = player_pos
        distance = math.hypot(player_x - dog_x, player_y - dog_y)

        if distance <= self.attack_distance + 5:
            self.perform_attack()

    def perform_attack(self):
        if not self.can_attack or self.attack_count >= self.attack_max:
            return

        player = LevelManager.get_instance().get_player()
        if player:
            player_candy = player.get_component("PlayerCandy")
            if player_candy:
                player_candy.take_candy(1)
                if player_candy.candy == 0:
                    self.attack_count = self.attack_max

        self.attack_count += 1
        self.cooldown_timer = self.attack_rate
        self.can_attack = False

    # --- Movement Logic ---
    def get_target_position(self):
        player_pos = LevelManager.get_instance().get_player_position()
        if self.attack_count < self.attack_max and self.attack_timer < self.attack_time and player_pos:
            return *player_pos, True
        return *self.home_position, False

    def calculate_movement_direction(self, target_x, target_y, hover):
        dog_x, dog_y = self.game_object.transform.get_world_position()
        dx = target_x - dog_x
        dy = target_y - dog_y
        distance = math.hypot(dx, dy)
        min_distance = self.attack_distance if hover else 1.0
        HOVER_RANGE = 2.0

        if distance > min_distance + (HOVER_RANGE if hover else 0):
            dir_x = dx / distance
            dir_y = dy / distance
        elif distance < min_distance - (HOVER_RANGE if hover else 0) and hover:
            dir_x = -dx / distance
            dir_y = -dy / distance
        elif hover:
            # Hover/circle around player
            dir_x = -dy / distance * 0.3
            dir_y = dx / distance * 0.3
        else:
            dir_x, dir_y = 0, 0

        return dir_x, dir_y

    def apply_movement(self, dir_x, dir_y, target_x, target_y, dt):
        dog_x, dog_y = self.game_object.transform.get_world_position()
        move_x = dir_x * self.move_speed * dt
        move_y = dir_y * self.move_speed * dt
        new_x = dog_x + move_x
        new_y = dog_y + move_y
        self.game_object.transform.set_local_position(new_x, new_y)

        # Flip sprite based on horizontal direction toward target
        dx = target_x - dog_x
        if abs(dx) > 0.1:
            self.sprite.flip_x = dx < 0
