import pygame

class Window():
    def __init__(self):
        self.size = [640, 480]
        self.caption = "Super Panda Commander Gold" +\
                        " - Now with PandaCloud + bonus TF2 hat!"
        self.fps = "30"

        self.running = True

        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.caption)
        self.clock = pygame.time.Clock()

        while(self.running):
            """Do Magic"""
            self.clock.tick()

    def quit(self):
        self.running = False
