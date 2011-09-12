from __future__ import print_function

from pyglet import resource
from pyglet import event
from pyglet import graphics
from pyglet.window import mouse, key

import data
import camera

class Level(event.EventDispatcher):
    def __init__(self, p_window):
        self.p_window = p_window
        winx, winy = self.p_window.get_size()
        self.camera = camera.Camera(0,0, winx, winy, 50)

        self.batch = graphics.Batch()
        

    def connect(self):
        self.p_window.push_handlers( self.on_update, self.on_draw, 
                                     self.on_key_press )

    def disconnect(self):
        self.p_window.pop_handlers()

    def on_update(self, dt):
        self.dispatch_event('level_update', dt, self.camera)

    def on_draw(self):
        self.p_window.clear()
        self.batch.draw()

    def on_key_press(self, symbol, modi):
        if symbol == key.ESCAPE:
            self.p_window.quit()
            return True

Level.register_event_type('level_update')

 
