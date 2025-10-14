from cogworks import Engine

from assets.scenes.level_1_scene import setup_level_1_scene

engine = Engine(width=800, height=600, caption="Trick or Treat Trouble")

setup_level_1_scene(engine)

engine.set_active_scene("Level 1")

engine.run()