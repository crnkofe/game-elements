"""
Sample color picking implementation.
"""

import pygame
from pygame.locals import QUIT
import util

class ColorPicker(object):

    def __init__(self, screen):
        self.screen = screen
        self.shown = False

    def handle_event(self, event):
        if event.type == QUIT:
            util.switch(util.Displays.MENU)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                util.switch(util.Displays.MENU)

    def draw(self, elapsed):
        pass
