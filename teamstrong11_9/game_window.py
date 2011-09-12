from __future__ import print_function

import pyglet

from level import Level
from pyglet import window
from pyglet import clock
import data
import settings
from shortcuts import *

# some dodgy code to call the 'update' function on every sprite
# every frame.

"""
def update(dt):
    map(lambda s: s.update(dt), sprites)

pyglet.clock.schedule_interval(update, 1/30.)
"""

#----------------------------------------------
# main game window. Checks for all of the keyboard events atm.

class GameWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super(GameWindow, self).__init__(*args, **kwargs)

        # Setup a clock for frame rate
        clock.set_fps_limit(settings.FPS_LIMIT)
        # Setup updates to run once per tick
        clock.schedule(self.update)
        # Create the level and connect
        self.create_level()

    def create_level(self):
        self.level = Level(self)
        self.level.connect()

    # Scheduled to run once per tick
    def update(self, dt):
        self.dispatch_event('on_update', dt)

    def quit(self):
        # pyglet exit variable built into pyglet.window.Window
        self.has_exit = True

GameWindow.register_event_type('on_update')
