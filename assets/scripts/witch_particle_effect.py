import weakref

from cogworks.components.particle_effect import ParticleEffect

from assets.scripts.level_manager import LevelManager


class WitchParticleEffect(ParticleEffect):
    def __init__(self, particle_amount: int = 8, lifetime=7):
        super().__init__(
            sprite_path="images/witch_particle.png",
            particle_amount=particle_amount,
            min_y=-10,
            max_y=10,
            scale_with_lifetime=True,
            fade_over_lifetime=True,
            rotate_over_lifetime=True,
            lifetime=lifetime,
            gravity=-10,
            move_speed=10,
            min_scale=0.7,
            max_scale=1.3,
        )

    def update(self, dt: float) -> None:
        super().update(dt)

        lm = LevelManager.get_instance()
        x, y = lm.get_player_position()
        self.game_object.transform.set_local_position(x, y)