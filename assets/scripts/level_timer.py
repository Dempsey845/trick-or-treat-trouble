from cogworks.components.script_component import ScriptComponent
from cogworks.components.ui.ui_label import UILabel
from cogworks.components.ui.ui_transform import UITransform


class LevelTimer(ScriptComponent):
    def __init__(self):
        super().__init__()
        self.level_time = 120.0  # 120 seconds = 2 hours
        self.timer = self.level_time
        self.label = None

    def start(self) -> None:
        self.game_object.add_component(UITransform(
            anchor="center", relative=True, x=0.5, y=0.05, width=0.15, height=0.05, debug=False
        ))
        self.label = UILabel("Time: 7:00 PM")
        self.game_object.add_component(self.label)

        self.timer = self.level_time

    def update(self, dt: float) -> None:
        self.timer -= dt
        if self.timer <= 0.0:
            self.game_object.scene.restart()
            self.timer = self.level_time

        total_hours = 2  # 7 PM to 9 PM
        elapsed_hours = (self.level_time - self.timer) / 60.0  # 60s = 1 hour
        current_hour = 7 + int(elapsed_hours)
        current_minute = int((elapsed_hours - int(elapsed_hours)) * 60)

        period = "PM"
        hour_display = current_hour
        if hour_display > 12:
            hour_display -= 12

        time_text = f"Time: {hour_display}:{current_minute:02d} {period}"
        self.label.set_text(time_text)
