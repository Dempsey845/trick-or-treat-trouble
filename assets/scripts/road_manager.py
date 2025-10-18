import random
from cogworks import GameObject
from cogworks.components.script_component import ScriptComponent

from assets.scripts.cogweb import Cobweb


class RoadManager(ScriptComponent):
    def __init__(self):
        super().__init__()
        self.web_scale = 2.5
        self.min_distance = 16 * self.web_scale + 10

        # Main road
        self.main_road_start_pos = (720, 290)
        self.main_road_end_pos = (1120, 1016)
        self.main_road_web_count = 8

        # Side roads
        self.side_roads = [
            {"start": (60, 285), "end": (644, 394), "count": 3},
            {"start": (1237, 285), "end": (1858, 394), "count": 3},
            {"start": (1237, 716), "end": (1858, 786), "count": 3},
            {"start": (60, 700), "end": (644, 794), "count": 3},
        ]

    def spawn_cob_web(self, x, y):
        cobweb = GameObject("Cobweb", z_index=2, x=x, y=y,
                            scale_x=self.web_scale, scale_y=self.web_scale)
        cobweb.add_component(Cobweb())
        self.game_object.scene.instantiate_game_object(cobweb)

    def spawn_webs_on_road(self, start_pos, end_pos, count, spawned_positions):
        for _ in range(count):
            for attempt in range(100):
                x = random.uniform(start_pos[0], end_pos[0])
                y = random.uniform(start_pos[1], end_pos[1])

                too_close = any(
                    ((x - sx) ** 2 + (y - sy) ** 2) ** 0.5 < self.min_distance
                    for sx, sy in spawned_positions
                )

                if not too_close:
                    self.spawn_cob_web(x, y)
                    spawned_positions.append((x, y))
                    break

    def start(self):
        spawned_positions = []

        # Spawn main road webs
        self.spawn_webs_on_road(self.main_road_start_pos, self.main_road_end_pos,
                                self.main_road_web_count, spawned_positions)

        # Spawn side road webs
        for road in self.side_roads:
            self.spawn_webs_on_road(road["start"], road["end"], road["count"],
                                    spawned_positions)
