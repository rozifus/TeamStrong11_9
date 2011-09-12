from __future__ import print_function

import pyglet
import settings
from game_window import GameWindow

def main():
    """ your app starts here
    """

    gameWindow = GameWindow(*settings.RESOLUTION)
    pyglet.app.run()


