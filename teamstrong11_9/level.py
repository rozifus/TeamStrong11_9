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
from countdown import Countdown
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
        self.enemies = []

        self.initialize()

    # Setup the level
    def initialize(self):
        self.player = Player(self, batch=self.batch)
        self.gravitoids.append(self.player)
        self.sprites.append(self.player)

        # a countdown clock. Countdown to success.
        self.timer = Countdown(self, batch=self.batch)
        self.sprites.append(self.timer)

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
        player_box = self.player.get_collision_box()
        for e in self.enemies:
            if e.get_collision_box().isCollide(*player_box.get_values()):
                self.handle_the_dead(e)

        self.do_gravity(dt)
        self.dispatch_event('on_level_update', dt, self.camera)
        self.game_strategy(dt)

    def game_strategy(self, dt):
        """
        Game strategising comes into play here.

        A countdown is created and then once the time is up, a new ghost
        appears and countdown clock begins ticking again.
        """
        if self.timer.alarm:
            self.timer.reset(random.randint(2, 15))
            enemy = Enemy(self, batch=self.batch)
            self.sprites.append(enemy)
            self.enemies.append(enemy)

    def do_gravity(self, dt):
        for g in self.gravitoids:
            if g.y <= self.surface_y:
                g.velocity_y = 0
                g.y = self.surface_y
                g.touch_ground = True
            else:
                g.velocity_y -= settings.GRAVITY * dt

    def char_punch(self, attack_box):
        """
        If a character punches an enemy, the enemy dies and goes to the
        naughty corner.
        """

        for e in self.enemies:
            if attack_box.isCollide(*e.get_collision_box().get_values()):
                self.player_is_victorious_with_punch(e)

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

    def player_is_victorious_with_punch(self, ghost):
        """
        The player has successfully punched the ghost!
        """
        ghost.set_dead()

        punched_ghosts = filter(lambda x: not x.won, self.ghosts_of_christmas_past)
        if len(punched_ghosts) >= 3:
            print("Winner winner: Chickns")
            raise SystemExit

        try:
            maxx = punched_ghosts[-1].ghost.x
        except IndexError:
            maxx = 0

        newx = maxx + ghost.width + 10
        ghost.x, ghost.y = newx, 50
        self.ghosts_of_christmas_past.append(
                            GhostOutcome(ghost, False))

    def handle_the_dead(self, ghost):
        """
        The ghost has hit our player! thats a bad thing.
        Put the ghost up on a victory tally somewhere..

        If there has been three dead already. Exit the game.
        """
        ghost.set_dead()

        victorious_ghosts = filter(lambda x: x.won, self.ghosts_of_christmas_past)
        if len(victorious_ghosts) >= 3:
            print("Dam u ded: Free times")
            raise SystemExit

        try:
            minx = victorious_ghosts[-1].ghost.x
        except IndexError:
            minx = settings.RESOLUTION[0]

        newx = minx - ghost.width - 10
        ghost.x, ghost.y = newx, 50
        self.ghosts_of_christmas_past.append(
                            GhostOutcome(ghost, True))

Level.register_event_type('on_level_update')
