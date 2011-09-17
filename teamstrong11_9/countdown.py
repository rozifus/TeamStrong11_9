import pyglet
from pyglet.window import key
from pyglet.image import ImageGrid, Animation

import settings
from shortcuts import *

#------------------------------------------------------------
# The countdown to success timer!

class Countdown(pyglet.sprite.Sprite):
    """
    A bar on the top of the screen to count down from a high number to a low
    number.
    """

    image_file = None

    def __init__(self, p_level, *args, **kws):
        self.images = ImageGrid(load(fp('countdown.png')), 6, 1)
        super(Countdown, self).__init__(self.images[-1], *args, **kws)
        self.parent = p_level

        self.x, self.y = 50, 500

        self.time = 0
        self.accumulated_time = 0
        self.running = False
        self.alarm = False
        self.steps = 0
        self.parent.push_handlers(self.on_level_update)

    def reset(self, time):
        """
        Reset the countdown with the maximum time given.
        """
        self.running = True
        self.time = time
        self.steps = time / 5.

    def on_level_update(self, dt, camera):
        """
        Work out if I need to change my image to the next bar bit.
        """
        if self.accumulated_time > self.time:
            self.alarm = True
            self.accumulated_time = 0
        else:
            self.accumulated_time += dt

        try:
            index = min(int(self.steps / self.accumulated_time), 5)
        except ZeroDivisionError:
            index = 0

        self.image = self.images[index]

