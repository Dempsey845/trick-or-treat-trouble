from cogworks.components.script_component import ScriptComponent
from cogworks.components.ui.ui_label import UILabel
from cogworks.components.ui.ui_transform import UITransform


class LevelTimer(ScriptComponent):
    def __init__(self):
        super().__init__()
        self.level_time = 120.0
        self.timer = self.level_time
        self.label = None

    def start(self) -> None:
        self.game_object.add_component(UITransform(anchor="center", relative=True, x=0.5, y=0.05, width=0.1, height=0.05, debug=True))
        self.label = UILabel("Time Left: ")
        self.game_object.add_component(self.label)

        self.timer = self.level_time

    def update(self, dt: float) -> None:
        self.timer -= dt

        if self.timer <= 0.0:
            self.timer = 0.0

        self.label.set_text(f"Time Left: {int(self.timer)}")


