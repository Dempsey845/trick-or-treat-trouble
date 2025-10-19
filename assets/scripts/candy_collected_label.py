from cogworks.components.script_component import ScriptComponent
from cogworks.components.ui.ui_label import UILabel

from assets.scripts.level_manager import LevelManager


class CandyCollectedLabel(ScriptComponent):
    def __init__(self):
        super().__init__()

    def start(self) -> None:
        candy_collected = LevelManager.candy_collected
        self.game_object.get_component(UILabel).set_text(f"You collected {candy_collected} candy!")