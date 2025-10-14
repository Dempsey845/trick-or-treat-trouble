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
        self.input_x = 0
        self.input_y = 0

        self.input = None
        self.rigidbody = None
        self.sprite = None

    def start(self):
        self.rigidbody = self.game_object.get_component(Rigidbody2D)
        self.input = InputManager.get_instance()
        self.sprite = self.game_object.get_component(Sprite)

    def update(self, dt: float):
        if not self.sprite:
            return

        # Reset input each frame
        self.input_x = 0
        self.input_y = 0

        if self.input.is_key_down(pygame.K_w):
            self.input_y = -1
        elif self.input.is_key_down(pygame.K_s):
            self.input_y = 1

        if self.input.is_key_down(pygame.K_a):
            self.input_x = -1
            self.sprite.flip_x = True
        elif self.input.is_key_down(pygame.K_d):
            self.input_x = 1
            self.sprite.flip_x = False

    def fixed_update(self, dt:float):
        rb = self.rigidbody

        if not rb:
            return

        magnitude = math.hypot(self.input_x, self.input_y)
        if magnitude > 0:
            norm_x = self.input_x / magnitude
            norm_y = self.input_y / magnitude
            rb.desired_velocity = norm_x * self.move_speed, norm_y * self.move_speed
        else:
            rb.desired_velocity = 0, 0

    def get_move_direction(self):
        return self.input_x, self.input_y