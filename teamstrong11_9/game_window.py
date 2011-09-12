from __future__ import print_function

import pyglet

from level import Level
from pyglet import window
from pyglet import clock
import data
import settings

#------------------------------------------------------------
# shortcuts.
fp = data.filepath
load = pyglet.image.load

#------------------------------------------------------------
# basic character.
batch = pyglet.graphics.Batch()
enemies = pyglet.graphics.Batch()

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

sprites = [

        Character(
            pyglet.image.ImageGrid(
                load(fp('character.png')), 1, 2), batch=batch),

        Enemy(
            pyglet.image.ImageGrid(
                load(fp('enemy.png')), 1, 2), batch=enemies)
]

# some dodgy code to call the 'update' function on every sprite
# every frame.

def update(dt):
    map(lambda s: s.update(dt), sprites)

pyglet.clock.schedule_interval(update, 1/30.)

#----------------------------------------------
# main game window. Checks for all of the keyboard events atm.

class GameWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super(GameWindow, self).__init__(*args, **kwargs)
        self.running = True
        self.create_level()
        self.background = load(fp('background.png'))
        clock.set_fps_limit(settings.FPS_LIMIT)
        clock.schedule(self.update)

    def create_level(self):
        self.level = Level(self)
        self.level.connect()

    def update(self, dt):
        self.dispatch_event('on_update', dt)

    def on_draw(self):
        self.clear()
        # background must be drawn first.
        self.background.blit(0, 0)
        batch.draw()
        enemies.draw()

    def on_key_press(self, symbol, modifiers):
        """
        Look for left and right arrows.
        """
        handlers = {
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
        sprites[0].left()

    def handle_right_down(self):
        """
        Move character right.
        """
        sprites[0].right()

    def quit(self):
        self.has_exit = True

GameWindow.register_event_type('on_update')
