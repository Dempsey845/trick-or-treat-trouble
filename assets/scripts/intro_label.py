from cogworks.components.script_component import ScriptComponent
from cogworks.components.ui.ui_label import UILabel
from assets.scripts.level_manager import LevelManager
import time


class IntroLabel(ScriptComponent):
    """
    Displays an intro text sequence with fade-in and fade-out transitions.
    """

    def __init__(self):
        super().__init__()
        self.label = None
        self.sequence = []
        self.current_index = 0
        self.last_change = 0
        self.wait_time = 0
        self.done = False
        self.time_to_finish = ""

        # Fade control
        self.fade_state = "idle"  # idle, fading_in, visible, fading_out
        self.fade_duration = 0.5  # seconds per fade
        self.visible_duration = 1.5  # seconds text stays visible before fading out

    def start(self) -> None:
        self.time_to_finish = "10PM" if LevelManager.difficulty == "easy" else "9PM"
        self.label = self.game_object.get_component(UILabel)
        self.label.set_text("")
        self.label.alpha = 0

        self.current_index = 0
        self.last_change = 0
        self.wait_time = 0
        self.done = False

        self.fade_state = "idle"

        self.sequence = [
            ("It's Halloween night...", 2.5),
            ("You're out trick or treating!", 2.5),
            (f"Go home for {self.time_to_finish}!", 2.5),
            ("Some houses will have treats...", 2.5),
            ("Others... might have tricks.", 3.0),
            ("Good luck!", 3.0),
        ]

        self.last_change = time.time()

    def update(self, delta_time: float) -> None:
        if self.done or not self.sequence:
            return

        current_time = time.time()

        # Handle fade state machine
        if self.fade_state == "idle":
            if self.current_index < len(self.sequence):
                text, self.wait_time = self.sequence[self.current_index]
                self.label.set_text(text)
                self.label.alpha = 0
                self.label.fade_in(speed=int(255 / (self.fade_duration * 60)))  # Approx fade per 60fps
                self.fade_state = "fading_in"
                self.last_change = current_time
            else:
                self.game_object.scene.engine.set_active_scene("Level 1")
                self.done = True

        elif self.fade_state == "fading_in":
            if self.label.alpha >= 255:
                self.fade_state = "visible"
                self.last_change = current_time

        elif self.fade_state == "visible":
            if current_time - self.last_change >= self.visible_duration:
                self.label.fade_out(speed=int(255 / (self.fade_duration * 60)))
                self.fade_state = "fading_out"

        elif self.fade_state == "fading_out":
            if self.label.alpha <= 0:
                self.current_index += 1
                self.fade_state = "idle"
