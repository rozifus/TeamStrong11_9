from __future__ import print_function

import pyglet

from game_window import GameWindow
import settings


def main():
    """ your app starts here
    """
    gameWindow = GameWindow(*settings.RESOLUTION)
    pyglet.app.run()
