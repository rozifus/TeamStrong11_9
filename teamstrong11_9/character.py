from __future__ import print_function
from math import copysign
from functools import wraps

import pyglet
from pyglet.window import key
from pyglet.image import ImageGrid, Animation
import settings
from shortcuts import *


#---------------------------------------------------

# Library code.

def must_be_alive(fn):
    @wraps(fn)
    def inner_fn(self, *args):
        if not self.alive:
            return
        return fn(self, *args)
    return inner_fn

def applyAnchor(img, x, y):
    if isinstance(img, pyglet.image.Animation):
        for f in img.frames:
            f.image.anchor_x = x
            f.image.anchor_y = y
    else:
        img.anchor_x = x
        img.anchor_y = y

#---------------------------------------------------

class PlayerMovement:
    def __init__(self):
        pass

class DefaultMove:
    def __init__(self, target):
        self.target = target
        
    def next(self, dt, keys):
        if keys:
            if keys[key.UP]:
                self.target.jump()
            elif keys[key.LEFT]:
                self.target.step_left()
            elif keys[key.RIGHT]:
                self.target.step_right()
        return True

class JumpMove:
    def __init__(self, target, jumppower, maxjump):
        self.target = target
        self.jumppower = jumppower 
        self.maxjump = maxjump
        # Make sure velocity isn't removed because you are touching the ground
        self.target.y += 2
        # Make sure you can't double jump
        self.target.touch_ground = False
       
    def next(self, dt, keys):
        if keys:
            if not keys[key.UP]:
                self.maxjump = 0 
            if keys[key.RIGHT]: self.target.step_right()
            if keys[key.LEFT]: self.target.step_left()
       
        if self.maxjump > 0:
            self.target.velocity_y = self.jumppower 
            self.maxjump -= 1 
            return True
        else: 
            return False

class LinearMoveX:
    def __init__(self, target, distance, rate):
        self.clocked = 0.0
        self.rate = rate
        self.distance = distance
        self.target = target

    def next(self, dt, keys):
        if keys:
            if keys[key.UP]:
                self.target.jump()
            if self.distance < 0:
                if not keys[key.LEFT]:
                    return False
            else:
                if not keys[key.RIGHT]:
                    return False

        self.clocked += dt
        while self.clocked > self.rate:
            self.target.x += self.distance
            self.clocked -= self.rate
        return True

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
        self.anim_default_left = self.anim_default.get_transform(True)
        super(Character, self).__init__(self.anim_default, *args, **kws)
        self.p_level = p_level
        self.movement = None
        self.keys = None
        self.velocity_y = 0
        self.touch_ground = True
        self.orientation_right = True

    def on_level_update(self, dt, camera):
        self.y += self.velocity_y * dt
        if self.movement:
            if not self.movement.next(dt, self.keys):
                self.movement = self.default_movement 
                if self.orientation_right:
                    self.image = self.anim_default
                else: self.image = self.anim_default_left
        

class Player(Character):
    image_file = 'character.png'
    def __init__(self, p_level, *args, **kws):
        super(Player, self).__init__(p_level, *args, **kws)
        ig_step = ImageGrid(load(fp('panda_bounce_test.png')), 1, 7)
        self.animation = self.anim_default
        self.anim_step_right = Animation.from_image_sequence(
                                ig_step, 0.1, True) 
        applyAnchor(self.anim_step_right, 25, 0)
        self.anim_step_left = self.anim_step_right.get_transform(True)
        # Convenience class for key handling, pushed to window
        self.keys = key.KeyStateHandler()
        self.default_movement = DefaultMove(self)
        self.movement = self.default_movement

        self.init()

    def init(self):
        self.x = 100
        self.y = 198
        self.p_level.push_handlers( self.on_level_update)
        self.p_level.p_window.push_handlers( self.keys )

    def step_left(self):
        self.orientation_right = False
        if self.touch_ground:
            self.movement = LinearMoveX(self, -3, 0.1)
            self.image = self.anim_step_left
        else: self.x -= 1

    def step_right(self):
        self.orientation_right = True 
        if self.touch_ground:
            self.movement = LinearMoveX(self, 3, 0.1)
            self.image = self.anim_step_right
        else: self.x += 1

    def jump(self):
        if self.touch_ground:
            self.movement = JumpMove(self, 200, 4)


class Enemy(pyglet.sprite.Sprite):
    """
    An enemy is no laughing matter.
    """
    image_file = 'enemy.png'

    def __init__(self, parent, *args, **kwargs):
        self.images = ImageGrid(load(fp(self.image_file)), 1, 2)
        super(Enemy, self).__init__(self.images[0], *args, **kwargs)
        self.parent = parent
        self.init()

    def init(self):
        self.alive = True
        self.x = 700
        self.y = 200
        self.parent.push_handlers(self.on_level_update)

    def set_dead(self):
        self.alive = False
        self.x = 700
        self.y = 400

    @must_be_alive
    def on_level_update(self, dt, camera):
        """
        Now try to head toward the player!.
        """
        player = self.parent.player

        deltax = player.x - self.x
        if abs(deltax) < 5:
            # ok I have hit the player.
            self.set_dead()

        distance = 50 * dt

        # only move the ghost guy if the player is not looking.
        if player.orientation_right and deltax < 0:
            pass
        else:
            self.x = self.x + copysign(min(distance, abs(deltax)), deltax)

        self.image = self.images[0]

        if isoffscreen(self.x, self.y):
            self.x, self.y = 700, 200

def isoffscreen(x, y):
    """
    Returns True if the (x, y) co-ordinate is off screen.
    """
    return (x < 0 or x > settings.RESOLUTION[0]
            or y < 0 or y > settings.RESOLUTION[1])

