import random
from cogworks import GameObject
from cogworks.components.script_component import ScriptComponent

from assets.scripts.candy import Candy
from assets.scripts.cogweb import Cobweb


class RoadManager(ScriptComponent):
    def __init__(self):
        super().__init__()
        self.web_scale = 2.5
        self.min_distance = 16 * self.web_scale + 10

        self.candy_scale = 2
        self.candy_size = 40 * self.candy_scale
        self.candy_min_distance = self.candy_size + 5  # Minimum distance between candy/cobwebs

        # Main road
        self.main_road_start_pos = (720, 290)
        self.main_road_end_pos = (1120, 1016)
        self.main_road_web_count = 8
        self.main_road_candy_count = 4

        # Side roads
        self.side_roads = [
            {"start": (60, 285), "end": (644, 394), "count": 3, "candy_count": 2},
            {"start": (1237, 285), "end": (1858, 394), "count": 3, "candy_count": 1},
            {"start": (1237, 716), "end": (1858, 786), "count": 3, "candy_count": 1},
            {"start": (60, 700), "end": (644, 794), "count": 3, "candy_count": 2},
        ]

    def spawn_cob_web(self, x, y):
        cobweb = GameObject("Cobweb", z_index=2, x=x, y=y,
                            scale_x=self.web_scale, scale_y=self.web_scale)
        cobweb.add_component(Cobweb())
        self.game_object.scene.instantiate_game_object(cobweb)

    def spawn_candy(self, x, y):
        candy = GameObject("Candy", z_index=1, x=x, y=y,
                           scale_x=self.candy_scale, scale_y=self.candy_scale)
        candy.add_component(Candy())
        self.game_object.scene.instantiate_game_object(candy)

    def spawn_objects_on_road(self, start_pos, end_pos, count, spawned_positions, object_type="web"):
        center_x, center_y = 1920 // 2, 1080 // 2
        safe_radius = 50

        for _ in range(count):
            for attempt in range(100):
                x = random.uniform(start_pos[0], end_pos[0])
                y = random.uniform(start_pos[1], end_pos[1])

                min_dist = self.min_distance if object_type == "web" else self.candy_min_distance

                too_close = any(
                    ((x - sx) ** 2 + (y - sy) ** 2) ** 0.5 < min_dist
                    for sx, sy in spawned_positions
                )

                too_close_to_center = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5 < safe_radius

                if not too_close and not too_close_to_center:
                    if object_type == "web":
                        self.spawn_cob_web(x, y)
                        spawned_positions.append((x, y))
                    else:
                        self.spawn_candy(x, y)
                        spawned_positions.append((x, y))
                    break

    def start(self):
        spawned_positions = []

        # Spawn main road webs
        self.spawn_objects_on_road(self.main_road_start_pos, self.main_road_end_pos,
                                   self.main_road_web_count, spawned_positions, object_type="web")
        # Spawn main road candy
        self.spawn_objects_on_road(self.main_road_start_pos, self.main_road_end_pos,
                                   self.main_road_candy_count, spawned_positions, object_type="candy")

        # Spawn side road webs and candy
        for road in self.side_roads:
            self.spawn_objects_on_road(road["start"], road["end"], road["count"],
                                       spawned_positions, object_type="web")
            self.spawn_objects_on_road(road["start"], road["end"], road["candy_count"],
                                       spawned_positions, object_type="candy")
