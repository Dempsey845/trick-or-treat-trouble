from assets.scripts.level_manager import LevelManager
from cogworks.components.script_component import ScriptComponent
from cogworks.components.ui.ui_label import UILabel
from cogworks.components.ui.ui_transform import UITransform


class LevelTimer(ScriptComponent):
    def __init__(self):
        super().__init__()

        self.level_time = 100.0

        self.timer = self.level_time
        self.label = None
        self.start_offset_minutes = 20

    def start(self) -> None:
        if LevelManager.difficulty == "easy":
            self.level_time = 160
        else:
            self.level_time = 100

        self.game_object.add_component(UITransform(
            anchor="center", relative=True, x=0.5, y=0.10, width=0.15, height=0.05, debug=False
        ))
        self.label = UILabel("Time: 7:15 PM", font_path="fonts/rainyhearts.ttf",)
        self.game_object.add_component(self.label)

        self.timer = self.level_time

        print(self.level_time)

    def update(self, dt: float) -> None:
        self.timer -= dt
        if self.timer <= 0.0:
            self.game_object.scene.engine.set_active_scene("Finish")
            self.timer = self.level_time

        elapsed_hours = (self.level_time - self.timer) / 60.0
        current_time_hours = 7 + (self.start_offset_minutes / 60) + elapsed_hours

        current_hour = int(current_time_hours)
        current_minute = int((current_time_hours - current_hour) * 60)

        period = "PM"
        hour_display = current_hour
        if hour_display > 12:
            hour_display -= 12

        time_text = f"Time: {hour_display}:{current_minute:02d} {period}"
        self.label.set_text(time_text)
