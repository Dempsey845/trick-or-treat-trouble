from cogworks import Engine

from assets.scenes.finish_scene import setup_finish_scene
from assets.scenes.introduction_scene import setup_introduction_scene
from assets.scenes.level_1_scene import setup_level_1_scene
from assets.scenes.menu_scene import setup_menu_scene

engine = Engine(fps=300, width=1280, height=720, fullscreen=True, caption="Trick or Treat Trouble")

setup_menu_scene(engine)
setup_introduction_scene(engine)
setup_level_1_scene(engine)
setup_finish_scene(engine)

engine.set_active_scene("Menu")

engine.run()