from __future__ import print_function

import pyglet
import settings

#------------------------------------------------------------
# basic character.
class Character(pyglet.sprite.Sprite):
    """
    A character is made from more than one image.
    Some for punching, some for walking etc.

    The left and right actions are called from the main window
    `on_key_press`. It is all very hardcoded. And i'm sure there is a
    way to push the handlers directly from the character instead of
    having the window do it.

    Every time the left or right button is pressed, toggle_man is called
    which swiches the "image" to blit for the sprite.
    """
    def __init__(self, imagegrid, *args, **kws):
        self.images = imagegrid
        super(Character, self).__init__(self.images[0], *args, **kws)
        self.init()

    def init(self):
        self.x = 100
        self.y = 200

    def toggle_man(self):
        self.images = list(reversed(self.images))

    def left(self):
        self.x = max(self.x - 2, 0)
        self.toggle_man()

    def right(self):
        self.x = min(self.x + 2, settings.RESOLUTION[0])
        self.toggle_man()

    def update(self, dt):
        self.image = self.images[0]

class Enemy(Character):
    """
    An enemy is no laughing matter.
    """
    def init(self):
        self.x = 700
        self.y = 200

    def update(self, dt):
        """
        Keep moving left!
        """
        self.x = self.x - 5 * dt
        self.toggle_man()
        self.image = self.images[0]


