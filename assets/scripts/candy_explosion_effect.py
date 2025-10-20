from cogworks.components.particle_effect import ParticleEffect


class CandyExplosionEffect(ParticleEffect):
    def __init__(self, particle_count: int = 1):
        super().__init__(
            sprite_path="images/candy.png",
            emission_rate=0.0,
            burst_count=particle_count,
            looping=False,
            duration=0.2,
            start_delay=0.0,
            simulation_space="world",
            gravity=-5,
            move_speed=80,
            min_x=-50,
            max_x=50,
            min_y=-50,
            max_y=50,
            min_scale=0.7,
            max_scale=1.3,
            scale_with_lifetime=True,
            fade_over_lifetime=True,
            rotate_over_lifetime=True,
            lifetime=2.0,
        )