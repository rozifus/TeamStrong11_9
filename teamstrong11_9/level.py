from __future__ import print_function

from pyglet import resource
from pyglet import event
from pyglet import graphics
from pyglet.window import mouse, key

import data
import camera
from character import Character, Enemy
from shortcuts import *

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

        self.initialize()

    # Setup the level
    def initialize(self):
        self.player = Character(batch=self.batch)
        self.sprites.append(self.player)

        #self.sprites.append(Enemy(batch=self.batch))

    # Connect the level's handlers, to the window's dispatchers
    def connect(self):
        self.p_window.push_handlers( self.on_update, self.on_draw, 
                                     self.on_key_press )

    # Pop the window's newest added handlers, hopefully this level's!
    def disconnect(self):
        self.p_window.pop_handlers()

    # Gets called once per tick by the game_window
    def on_update(self, dt):
        #not being used currently
        self.dispatch_event('level_update', dt, self.camera)
        #being used currently
        for s in self.sprites:
            s.update(dt)

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
                pyglet.window.key.LEFT: self.handle_left_down,
                pyglet.window.key.RIGHT: self.handle_right_down}

        try:
            handler = handlers[symbol]
        except KeyError:
            pass
        else:
            handler()

    def handle_left_down(self):
        """
        Move character left.
        """
        if self.player:
            self.player.left()

    def handle_right_down(self):
        """
        Move character right.
        """
        if self.player:
            self.player.right()
    
    def handle_quit(self):
        self.p_window.quit()

Level.register_event_type('level_update')

 
