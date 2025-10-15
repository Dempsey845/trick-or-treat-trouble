from cogworks.components.script_component import ScriptComponent
from cogworks.components.ui.ui_label import UILabel
from cogworks.components.ui.ui_transform import UITransform


class TrickOrTreatPrompt(ScriptComponent):
    def __init__(self, trick=False):
        super().__init__()
        self.trick = trick
        self.lifespan = 2
        self.lifetime = 0

    def start(self):
        ui_transform = UITransform(
            x=0.5, y=0.1, width=1, height=0.1, anchor="center", debug=False
        )
        self.game_object.add_component(ui_transform)

        text = "Trick!" if self.trick else "Treat!"
        color = (255, 0, 0) if self.trick else (0, 255, 0)

        label = UILabel(text, font_size=40, color=color)
        self.game_object.add_component(label)

    def update(self, dt: float) -> None:
        self.lifetime += dt

        if self.lifetime > self.lifespan:
            self.game_object.destroy()
