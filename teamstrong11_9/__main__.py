from __future__ import print_function

import pyglet
from game_window import GameWindow

res = (800, 600)

def main():
    """ your app starts here
    """
    
    gameWindow = GameWindow(*res)
    pyglet.app.run()    
