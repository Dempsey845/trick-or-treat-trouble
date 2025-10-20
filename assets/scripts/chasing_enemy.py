import math
from cogworks.components.script_component import ScriptComponent
from assets.scripts.level_manager import LevelManager


class ChasingEnemy(ScriptComponent):
    def __init__(self, home_position, move_speed=180, attack_distance=55, attack_rate=1,
                 attack_max=2, attack_time=7.0):
        super().__init__()
        # Movement
        self.home_position = home_position
        self.move_speed = move_speed

        # Attack
        self.attack_distance = attack_distance
        self.attack_rate = attack_rate
        self.cooldown_timer = attack_rate
        self.can_attack = False
        self.attack_max = attack_max
        self.attack_count = 0
        self.attack_time = attack_time
        self.attack_timer = 0.0

        self.sprite = None

    def start_attack_cooldown(self, duration: float = 3.0):
        """Prevents attacking for a specified duration (default 3 seconds)."""
        self.cooldown_timer = duration
        self.can_attack = False

    def update(self, dt: float) -> None:
        self.attack_timer += dt
        self.handle_attack_cooldown(dt)

        target_x, target_y, hover = self.get_target_position()
        dir_x, dir_y = self.calculate_movement_direction(target_x, target_y, hover)
        self.apply_movement(dir_x, dir_y, target_x, target_y, dt)

        # Destroy entity when back home and not hovering
        if not hover:
            ex, ey = self.game_object.transform.get_world_position()
            if math.hypot(target_x - ex, target_y - ey) < 5:
                self.on_reached_home(dt)

    def perform_attack(self):
        """Called when an attack should occur. Override in child class."""
        pass

    def on_reached_home(self, dt):
        if self.sprite:
            FADE_SPEED = 255 / 1  # fade out in 1 seconds
            self.sprite.alpha -= FADE_SPEED * dt
            if self.sprite.alpha < 10:
                self.game_object.destroy()
        else:
            self.game_object.destroy()

    def handle_attack_cooldown(self, dt: float):
        if not self.can_attack:
            self.cooldown_timer -= dt
            if self.cooldown_timer <= 0:
                self.can_attack = True

        if self.attack_count >= self.attack_max or self.attack_timer >= self.attack_time:
            return

        player_pos = LevelManager.get_instance().get_player_position()
        if not player_pos:
            return

        ex, ey = self.game_object.transform.get_world_position()
        px, py = player_pos
        distance = math.hypot(px - ex, py - ey)

        if distance <= self.attack_distance + 10:
            self.perform_attack()

    def get_target_position(self):
        player_pos = LevelManager.get_instance().get_player_position()
        if self.attack_count < self.attack_max and self.attack_timer < self.attack_time and player_pos:
            return *player_pos, True
        return *self.home_position, False

    def calculate_movement_direction(self, target_x, target_y, hover):
        ex, ey = self.game_object.transform.get_world_position()
        dx = target_x - ex
        dy = target_y - ey
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
            dir_x = -dy / distance * 0.3
            dir_y = dx / distance * 0.3
        else:
            dir_x, dir_y = 0, 0

        return dir_x, dir_y

    def apply_movement(self, dir_x, dir_y, target_x, target_y, dt):
        ex, ey = self.game_object.transform.get_world_position()
        new_x = ex + dir_x * self.move_speed * dt
        new_y = ey + dir_y * self.move_speed * dt
        self.game_object.transform.set_local_position(new_x, new_y)

        if self.sprite:
            dx = target_x - ex
            if abs(dx) > 0.1:
                self.sprite.flip_x = dx < 0
