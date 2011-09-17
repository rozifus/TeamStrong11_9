from __future__ import print_function
from collections import namedtuple
import math
import random

from pyglet import resource
from pyglet import event
from pyglet import graphics
from pyglet.window import mouse, key

import data
import camera
from character import Player, Enemy
from shortcuts import *
import settings

GhostOutcome = namedtuple("GhostOutcome", "ghost won")

class Level(event.EventDispatcher):
    def __init__(self, p_window):
        self.p_window = p_window
        winx, winy = self.p_window.get_size()
        self.camera = camera.Camera(0,0, winx, winy, 50)

        # Setup background, draw batch, spritelist, player
        self.background = load(fp('background.png')) 
        self.batch = graphics.Batch()
        self.sprites = []
        self.player = None
        self.surface_y = 195 
        self.gravitoids = []

        self.initialize()

    # Setup the level
    def initialize(self):
        self.player = Player(self, batch=self.batch)
        self.gravitoids.append(self.player)
        self.sprites.append(self.player)

        self.sprites.append(Enemy(self, batch=self.batch))

        # winning and losing ghosts.
        # will be a list of GhostOutcome tuples (ghost, win? True/False)
        self.ghosts_of_christmas_past = []

    # Connect the level's handlers, to the window's dispatchers
    def connect(self):
        self.p_window.push_handlers( self.on_update, self.on_draw )

    # Pop the window's newest added handlers, hopefully this level's!
    def disconnect(self):
        self.p_window.pop_handlers()

    # Gets called once per tick by the game_window
    def on_update(self, dt):
        self.do_gravity(dt)
        self.dispatch_event('on_level_update', dt, self.camera)
        self.game_strategy(dt)

    def game_strategy(self, dt):
        """
        Game strategising comes into play here.

        At the moment I have it so that a new enemy appears quite randomly
        actually. Quite randomly indeed.
        """
        new_ghost = random.randint(1, settings.FPS_LIMIT * 20)
        if not new_ghost == 5:
            return

        self.sprites.append(Enemy(self, batch=self.batch))

    def do_gravity(self, dt):
        for g in self.gravitoids:
            if g.y <= self.surface_y:
                g.velocity_y = 0
                g.y = self.surface_y
                g.touch_ground = True
            else:
                g.velocity_y -= settings.GRAVITY * dt

    # Gets called once per tick by the game loop
    def on_draw(self):
        self.p_window.clear()
        self.background.blit(0,0)
        self.batch.draw()

    # Called by dispatcher on game_window, when required
    def on_key_press(self, symbol, modifiers):
        """
        Look for left and right arrows.
        """
        handlers = {
                key.ESCAPE: self.handle_quit,
                pyglet.window.key.UP: self.handle_up_down,
                pyglet.window.key.LEFT: self.handle_left_down,
                pyglet.window.key.RIGHT: self.handle_right_down}

        try:
            handler = handlers[symbol]
        except KeyError:
            pass
        else:
            handler()

    def handle_up_down(self):
        """
        Make character jump.
        """
        if self.player:
            if not self.player.movement:
                self.player.jump()

    def handle_left_down(self):
        """
        Move character left.
        """
        if self.player:
            if not self.player.movement:
                self.player.step_left()

    def handle_right_down(self):
        """
        Move character right.
        """
        if self.player:
            if not self.player.movement:
                self.player.step_right()

    def handle_quit(self):
        self.p_window.quit()

    def handle_the_dead(self, ghost):
        """
        The ghost has hit our player! thats a bad thing.
        Put the ghost up on a victory tally somewhere..
        """

        try:
            minx = self.ghosts_of_christmas_past[-1].ghost.x
        except IndexError:
            minx = settings.RESOLUTION[0]

        newx = minx - ghost.width - 10
        ghost.x, ghost.y = newx, 50
        self.ghosts_of_christmas_past.append(
                            GhostOutcome(ghost, True))

Level.register_event_type('on_level_update')

def poisson(actual, mean):
    # naive:   math.exp(-mean) * mean**actual / factorial(actual)

    # iterative, to keep the components from getting too large or small:
    p = math.exp(-mean)
    for i in xrange(actual):
        p *= mean
        p /= i+1
    return p
