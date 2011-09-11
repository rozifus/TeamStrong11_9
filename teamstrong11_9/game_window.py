from __future__ import print_function

from pyglet import window
from level import Level

class GameWindow(window.Window):
    def __init__(self, *args, **kwargs):
        super(GameWindow, self).__init__(*args, **kwargs)
        self.running = True
        self.create_level()
        
    def create_level(self):
        self.level = Level(self)
        self.level.connect()

    def quit(self):
        self.running = False
        print("Not implemented yet...")
