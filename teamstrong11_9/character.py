from __future__ import print_function

import pyglet
from pyglet.image import ImageGrid, Animation
import settings
from shortcuts import *


def applyAnchor(img, x, y):
    if isinstance(img, pyglet.image.Animation):
        for f in img.frames:
            f.image.anchor_x = x
            f.image.anchor_y = y
    else:
        img.anchor_x = x
        img.anchor_y = y

class linearMoveX:
    def __init__(self, target, distance, steps, rate):
        self.clocked = 0.0
        self.rate = rate
        self.steps = steps
        self.distance = distance
        self.target = target

    def next(self, dt):
        self.clocked += dt
        if self.steps > 0:
            while self.clocked > self.rate:
                self.target.x += self.distance
                self.clocked -= self.rate
                self.steps -= 1
                return True
            return True
        else:
            return False

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

    image_file = None

    def __init__(self, p_level, *args, **kws):
        self.anim_default = Animation.from_image_sequence(ImageGrid(load(fp(
                    self.image_file)), 1, 1), 5, True)
        applyAnchor(self.anim_default, 25, 0)
        super(Character, self).__init__(self.anim_default, *args, **kws)
        self.p_level = p_level
        self.movement = None

    def on_level_update(self, dt, camera):
        if self.movement:
            if not self.movement.next(dt):
                self.movement = None

class Player(Character):
    image_file = 'character.png'
    def __init__(self, p_level, *args, **kws):
        super(Player, self).__init__(p_level, *args, **kws)
        ig_step = ImageGrid(load(fp('panda_bounce_test.png')), 1, 7)
        self.animation = self.anim_default
        self.anim_step_right = Animation.from_image_sequence(
                                ig_step, 0.1, False)
        applyAnchor(self.anim_step_right, 25, 0)
        self.anim_step_left = self.anim_step_right.get_transform(True)

        self.init()

    def init(self):
        self.x = 100
        self.y = 198
        self.p_level.push_handlers( self.on_level_update)

    def step_left(self):
        self.movement = linearMoveX(self, -3, 7, 0.1)
        self.image = self.anim_step_left

    def step_right(self):
        self.movement = linearMoveX(self, 3, 7, 0.1)
        self.image = self.anim_step_right


class Enemy(Character):
    """
    An enemy is no laughing matter.
    """
    image_file = 'enemy.png'

    def init(self):
        self.x = 700
        self.y = 200
        self.p_level.push_handlers(self.on_level_update)

    def on_level_update(self, dt, camera):
        """
        Keep moving left!
        """
        self.x = self.x - 5 * dt
        self.image = self.images[0]


