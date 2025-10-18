import weakref

from cogworks import GameObject
from cogworks.components.script_component import ScriptComponent
from cogworks.components.transform import Transform


class CameraController(ScriptComponent):
    """
    CameraController allows a camera to follow a target Transform with optional smoothing and offsets.
    """

    def __init__(
        self,
        target_object: GameObject,
        offset_x: float = 0,
        offset_y: float = 0,
        smoothing: float = 5.0,
        fixed: bool = False,
        max_y: float = None,
        max_x: float = None,
        min_x: float = None,
        min_y: float = None
    ):
        """
        Args:
            target_object (GameObject): The target GameObject.
            offset_x (float): Horizontal offset from the target position.
            offset_y (float): Vertical offset from the target position.
            smoothing (float): How fast the camera follows the target. Higher = snappier.
            fixed (bool): use fixed_update(). Good for following physics objects.
            max_y (float): Optional maximum y value for the camera.
            max_x (float): Optional maximum x value for the camera.
            min_x (float): Optional minimum x value for the camera.
            min_y (float): Optional minimum y value for the camera.
        """
        super().__init__()
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.smoothing = smoothing
        self.camera_component_ref = None
        self.target_object_ref = weakref.ref(target_object)
        self.target_transform_ref = None
        self.fixed = fixed

        # Clamp boundaries
        self.max_y = max_y
        self.max_x = max_x
        self.min_x = min_x
        self.min_y = min_y

    def start(self):
        self.camera_component_ref = weakref.ref(self.game_object.scene.camera_component)

    def update(self, dt: float) -> None:
        if not self.fixed:
            self.control(dt)

    def fixed_update(self, dt: float) -> None:
        if self.fixed:
            self.control(dt)

    def control(self, dt):
        camera_component = self.camera_component_ref()
        if not camera_component:
            return

        target_transform = self.target_object_ref().transform
        if not target_transform or not target_transform.exists():
            return

        width, height = self.game_object.scene.get_window_size()

        # Target position with offset
        target_x = target_transform.local_x + self.offset_x
        target_y = target_transform.local_y + self.offset_y

        # Current camera center
        current_x = camera_component.offset_x + (width / 2) / camera_component.zoom
        current_y = camera_component.offset_y + (height / 2) / camera_component.zoom

        # Smoothly interpolate towards target
        lerp_x = current_x + (target_x - current_x) * min(self.smoothing * dt, 1)
        lerp_y = current_y + (target_y - current_y) * min(self.smoothing * dt, 1)

        # Clamp to bounds if specified
        if self.max_x is not None:
            lerp_x = min(lerp_x, self.max_x)
        if self.min_x is not None:
            lerp_x = max(lerp_x, self.min_x)
        if self.max_y is not None:
            lerp_y = min(lerp_y, self.max_y)
        if self.min_y is not None:
            lerp_y = max(lerp_y, self.min_y)

        # Center camera on the interpolated position
        camera_component.center_on(lerp_x, lerp_y, width, height)
