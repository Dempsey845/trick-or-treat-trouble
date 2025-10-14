from cogworks.components.script_component import ScriptComponent
from cogworks.components.sprite_animation import SpriteAnimation

from assets.scripts.player_movement import PlayerMovement


class PlayerAnimationController(ScriptComponent):
    def __init__(self):
        super().__init__()
        self.sprite_animation = None
        self.player_movement = None
        self.current_animation = None
        self.last_direction = (1, 0)

    def start(self):
        self.sprite_animation = SpriteAnimation()

        # Idle animations
        self.sprite_animation.add_animation("SideIdle", "images/player/idle/side/idle.png", 1, 5, 0.2)
        self.sprite_animation.add_animation("DownIdle", "images/player/idle/down/idle.png", 6, 9, 0.2)
        self.sprite_animation.add_animation("UpIdle", "images/player/idle/up/idle.png", 10, 13, 0.2)

        # Walk animations
        self.sprite_animation.add_animation("SideWalk", "images/player/walk/side/walk.png", 1, 8, 0.1)
        self.sprite_animation.add_animation("DownWalk", "images/player/walk/down/walk.png", 9, 16, 0.1)
        self.sprite_animation.add_animation("UpWalk", "images/player/walk/up/walk.png", 17, 24, 0.1)

        self.game_object.add_component(self.sprite_animation)

        self.player_movement = self.game_object.get_component(PlayerMovement)

        # Start default state
        self.sprite_animation.set_animation("SideIdle")
        self.current_animation = "SideIdle"

    def update(self, dt: float):
        if not self.sprite_animation or not self.player_movement:
            return

        move_direction = self.player_movement.get_move_direction()
        moving = move_direction != (0, 0)

        # Update last non-zero direction if moving
        if moving:
            self.last_direction = move_direction

        dir_x, dir_y = self.last_direction

        # Decide whether to play idle or walk animations
        if dir_y < 0:
            new_anim = "UpWalk" if moving else "UpIdle"
        elif dir_y > 0:
            new_anim = "DownWalk" if moving else "DownIdle"
        else:
            new_anim = "SideWalk" if moving else "SideIdle"

        # Update animation only when it changes
        if new_anim != self.current_animation:
            self.sprite_animation.set_animation(new_anim)
            self.current_animation = new_anim
