import weakref
from cogworks.components.particle_effect import ParticleEffect
from assets.scripts.level_manager import LevelManager


class WitchParticleEffect(ParticleEffect):
    def __init__(self):
        super().__init__(
            sprite_path="images/witch_particle.png",
            emission_rate=3.33,      # about 1 every 0.3s
            duration=7.0,
            looping=False,
            simulation_space="local",
            gravity=-10,
            move_speed=10,
            min_x=-10,
            max_x=10,
            min_y=-20,
            max_y=20,
            min_scale=0.7,
            max_scale=1.3,
            scale_with_lifetime=True,
            fade_over_lifetime=True,
            rotate_over_lifetime=True,
            lifetime=1.5,
        )
        self.follow_smoothness = 5.0

    def update(self, dt: float) -> None:
        super().update(dt)

        lm = LevelManager.get_instance()
        target_x, target_y = lm.get_player_position()
        current_x, current_y = self.game_object.transform.get_local_position()

        # Smoothly move towards player
        new_x = current_x + (target_x - current_x) * dt * self.follow_smoothness
        new_y = current_y + (target_y - current_y) * dt * self.follow_smoothness

        self.game_object.transform.set_local_position(new_x, new_y)
