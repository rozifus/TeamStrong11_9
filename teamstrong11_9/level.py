from __future__ import print_function

from pyglet import resource
from pyglet import event
from pyglet.window import mouse, key

import data
import camera

class Level(event.EventDispatcher):
    def __init__(self, p_window):
        self.p_window = p_window
        winx, winy = self.p_window.get_size()
        self.camera = camera.Camera(0,0, winx, winy, 50)

    def connect(self):
        self.p_window.push_handlers( self.on_draw , self.on_key_press )

    def disconnect(self):
        self.p_window.pop_handlers()

    def on_draw(self):
        self.dispatch_event('level_draw', self.camera)

    def on_key_press(self, symbol, modi):
        if symbol == key.ESCAPE:
            self.p_window.quit()
            return True

Level.register_event_type('level_draw')

 
