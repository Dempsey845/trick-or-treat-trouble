from cogworks.components.script_component import ScriptComponent
from cogworks.components.ui.ui_label import UILabel
from cogworks.components.ui.ui_transform import UITransform


class InteractPrompt(ScriptComponent):
    def __init__(self, x, y):
        super().__init__()
        self.x, self.y = x, y

    def start(self):
        ui_transform = UITransform(
            x=self.x, y=self.y, width=40, height=40, anchor="center", world_space=True, debug=False
        )
        self.game_object.add_component(ui_transform)
        label = UILabel("E", font_size=40, color=(255, 255, 255))
        self.game_object.add_component(label)

