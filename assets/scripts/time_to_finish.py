from assets.scripts.level_manager import LevelManager
from cogworks.components.ui.ui_label import UILabel

from cogworks.components.script_component import ScriptComponent


class TimeToFinish(ScriptComponent):
    def __init__(self):
        super().__init__()

    def start(self) -> None:
        time_text = "9PM"
        if LevelManager.difficulty == "easy":
            time_text = "10PM"
        self.game_object.get_component(UILabel).set_text(f"Time To Finish: {time_text}")