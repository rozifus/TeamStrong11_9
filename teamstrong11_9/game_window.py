from __future__ import print_function

from pyglet import window
from pyglet import clock
from level import Level
import settings

class GameWindow(window.Window):
    def __init__(self, *args, **kwargs):
        super(GameWindow, self).__init__(*args, **kwargs)
        self.running = True
        self.create_level()
        clock.set_fps_limit(settings.FPS_LIMIT)
        clock.schedule(self.update)
        
    def create_level(self):
        self.level = Level(self)
        self.level.connect()

    def update(self, dt):
        self.dispatch_event('on_update', dt)

    def quit(self):
        self.has_exit = True

GameWindow.register_event_type('on_update')


