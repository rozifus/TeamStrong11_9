from __future__ import print_function
from functools import partial

import pyglet
from pyglet.window import mouse, key

from level import Level
from pyglet import window
from pyglet import clock
import data
import settings
from shortcuts import *

import kytten

#----------------------------------------------
# main game window. Checks for all of the keyboard events atm.

def show_help(window, batch, group, theme):

    document = pyglet.text.decode_attributed(
            '{bold True}Altered Panda{bold False}[ESC back]\n\n'
            'Try to punch [SPACE] the mutated versions of yourself.\n'
            'The altered pandas only move when your back is turned')

    dialog = kytten.Dialog(
            kytten.Frame(
                kytten.Document(document, width=300, height=150)),
            window=window, batch=batch, group=group,
            anchor=kytten.ANCHOR_CENTER,
            theme=theme, on_escape=lambda dialog:dialog.teardown())

class GameWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super(GameWindow, self).__init__(*args, **kwargs)
        self.init(*args, **kwargs)


    def init(self, *args, **kwargs):
        # Setup a clock for frame rate
        clock.set_fps_limit(settings.FPS_LIMIT)
        # Setup updates to run once per tick
        if kwargs.get('noreset', True):
            clock.schedule(self.update)

        #---------------------------------------------------------
        # MENU.

        # set up a menu system. It is a hack.
        # don't let anyone else tell you otherwise.

        self.menubatch = pyglet.graphics.Batch()
        self.menugroup = pyglet.graphics.OrderedGroup(1)
        self.bggroup = pyglet.graphics.OrderedGroup(0)
        theme = kytten.Theme(fp('theme'))

        menu_choices = {
                'Play Game': self.remove_menu_load_level,
                'Help!'    : partial(show_help, self,
                                     self.menubatch, self.menugroup, theme),
                'Quit'     : pyglet.app.exit,
        }

        def on_select(choice):
            menu_choices.get(choice)()

        self.background = load(fp('background.png'))

        self.dialog = kytten.Dialog(
                kytten.TitleFrame("Altered Panda",
                    kytten.VerticalLayout([
                        kytten.Menu(options=[
                            "Play Game",
                            "Help!",
                            "Quit",],
                            on_select=on_select),
                    ])
                ),
                window=self, batch=self.menubatch,
                group=self.menugroup, anchor=kytten.ANCHOR_TOP_LEFT,
                theme=theme
        )
        self.do_draw = True

    def remove_menu_load_level(self):
        self.do_draw = False
        self.pop_handlers()
        self.create_level()

    def on_draw(self):
        if self.do_draw:
            self.clear()
            self.background.blit(0, 0)
            self.menubatch.draw()

            # for now don't show the menu.. I hate clicking on it.
            #self.remove_menu_load_level()

    def create_level(self):
        self.level = Level(self)
        # Get level to push its handlers to us
        self.level.connect()

    # Scheduled to run once per tick
    def update(self, dt):
        self.dispatch_event('on_update', dt)

    def reset(self):
        self.level.disconnect()
        self.init(noreset=False)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            return self.reset()

        return super(GameWindow, self).on_key_press(symbol, modifiers)

    def quit(self):
        # pyglet exit variable built into pyglet.window.Window
        self.has_exit = True

# Allows handlers to be pushed to the game_window dispatcher
GameWindow.register_event_type('on_update')
