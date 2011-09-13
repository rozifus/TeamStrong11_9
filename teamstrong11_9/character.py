from __future__ import print_function

import pyglet
from pyglet.image import ImageGrid
import settings
from shortcuts import *

#------------------------------------------------------------
# basic character.

class Anim(object):
    def __init__(self, imagegrid, rate, repeat=False):
        self.repeat = repeat
        self.rate = rate
        self.imagegrid = imagegrid
        self.image = imagegrid[0]
        self.rate_count = rate 
        self.img_count = 0

    def update(self):
        self.rate_count -= 1  
        if self.rate_count < 1:
            self.img_count += 1
            self.rate_count = self.rate
            if self.img_count < len(self.imagegrid):
                self.image = self.imagegrid[self.img_count]
            elif self.repeat: 
                self.reset()
            else:
                self.image = None 

    def reset(self):
        self.img_count = 0
        self.rate_count = self.rate
        self.image = self.imagegrid[self.img_count]
 
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
    def __init__(self, *args, **kws):
        self.default = Anim(ImageGrid(load(fp(
                    'character.png')), 1,2), 100, True)
        super(Character, self).__init__(self.default.image, *args, **kws)
        self.anim = None
        self.movement = None
        self.init()
        self.anim_move = Anim(ImageGrid(load(fp(
                    'panda_bounce_test.png')), 1, 7), 5)
        self.anim = self.default

    def init(self):
        self.x = 100
        self.y = 200

    def left(self):
        self.x = max(self.x - 2, 0)
        self.anim = self.anim_move
        self.anim.reset()

    def right(self):
        self.x = min(self.x + 2, settings.RESOLUTION[0])
        self.anim = self.anim_move
        self.anim.reset()

    def update(self, dt):
        self.anim.update()
        if self.anim.image != None:
            self.image = self.anim.image
        else: 
            self.anim = self.default
            self.anim.reset()

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
        self.image = self.images[0]


