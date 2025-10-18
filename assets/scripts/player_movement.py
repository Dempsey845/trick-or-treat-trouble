import math

import pygame
from cogworks.components.rigidbody2d import Rigidbody2D
from cogworks.components.script_component import ScriptComponent
from cogworks.components.sprite import Sprite
from cogworks.pygame_wrappers.input_manager import InputManager


class PlayerMovement(ScriptComponent):
    def __init__(self, move_speed=200):
        super().__init__()
        self.move_speed = move_speed
        self.move_speed_multiplier = 1
        self.input_x = 0
        self.input_y = 0

        self.input = None
        self.rigidbody = None
        self.sprite = None

        self.invert_multiplier = 1  # 1 = normal, -1 = inverted
        self.invert_timer = 0.0

    def start(self):
        self.rigidbody = self.game_object.get_component(Rigidbody2D)

        self.input = InputManager.get_instance()
        self.sprite = self.game_object.get_component(Sprite)

    def update(self, dt: float):
        if not self.sprite:
            return

        # Update invert timer
        if self.invert_timer > 0:
            self.invert_timer -= dt
            if self.invert_timer <= 0:
                self.invert_multiplier = 1

        # Reset input each frame
        self.input_x = 0
        self.input_y = 0

        if self.input.is_key_down(pygame.K_w):
            self.input_y = -1
        elif self.input.is_key_down(pygame.K_s):
            self.input_y = 1

        if self.input.is_key_down(pygame.K_a):
            self.input_x = -1
            self.sprite.flip_x = self.invert_multiplier == 1
        elif self.input.is_key_down(pygame.K_d):
            self.input_x = 1
            self.sprite.flip_x = not self.invert_multiplier == 1

        self.check_bounds()

    def fixed_update(self, dt: float):
        rb = self.rigidbody
        if not rb:
            return

        magnitude = math.hypot(self.input_x, self.input_y)
        if magnitude > 0:
            norm_x = self.input_x / magnitude
            norm_y = self.input_y / magnitude
            rb.desired_velocity = (
                norm_x * self.move_speed * self.move_speed_multiplier * self.invert_multiplier,
                norm_y * self.move_speed * self.move_speed_multiplier * self.invert_multiplier
            )
        else:
            rb.desired_velocity = 0, 0

    def check_bounds(self):
        left_bound = 20
        right_bound = 1900
        top_bound = 20
        bottom_bound = 1040

        x, y = self.game_object.transform.get_local_position()

        move_x = self.input_x * self.invert_multiplier
        move_y = self.input_y * self.invert_multiplier

        if x < left_bound and move_x < 0:
            self.input_x = 0
        elif x > right_bound and move_x > 0:
            self.input_x = 0

        if y < top_bound and move_y < 0:
            self.input_y = 0
        elif y > bottom_bound and move_y > 0:
            self.input_y = 0

    def invert_movement(self, duration: float):
        self.invert_multiplier = -1
        self.invert_timer = duration

    def get_move_direction(self):
        return self.input_x * self.invert_multiplier, self.input_y * self.invert_multiplier