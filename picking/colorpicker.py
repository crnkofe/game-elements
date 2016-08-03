"""
Sample color picking implementation.
"""

import os
import random
import pygame
from pygame.locals import QUIT
import util

class PickableSmiley(object):

    def __init__(self, screen, pos):
        self.screen = screen
        self.pos = pos
        self.selected = False
        self.img = pygame.image.load(
            os.path.join('./assets/images/picking', 'smile.png')
        )

    def draw(self, elapsed):
        self.screen.blit(self.img, self.pos)

    def bounding_box(self):
        rect = self.img.get_rect().size
        return self.pos[0], self.pos[1], rect[0], rect[1]

    def within_bounds(self, pos):
        x, y, w, h = self.bounding_box()
        if pos[0] >= x and pos[0] <= x + w:
            pass
        else:
            return False
        if pos[1] >= y and pos[1] <= y + h:
            pass
        else:
            return False
        return True


class ColorPicker(object):

    def __init__(self, screen):
        self.screen = screen
        self.shown = False
        self.background = self._load_img(
            os.path.join('./assets/images/picking', 'ozadje.png')
        )
        self.smileys = [PickableSmiley(screen, (random.randint(100, 600), random.randint(100, 600))) for x in range(5)]

    def _load_img(self, full_path):
        image = pygame.image.load(full_path)
        return pygame.transform.scale(image, (800, 600))

    def handle_event(self, event):
        if event.type == QUIT:
            util.switch(util.Displays.MENU)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                util.switch(util.Displays.MENU)
        if event.type == pygame.MOUSEBUTTONUP:
            loc = pygame.mouse.get_pos()
            for smiley in self.smileys:
                smiley.selected = smiley.within_bounds(loc)

    def draw(self, elapsed):
        self.screen.blit(self.background, (0,0))
        for smiley in self.smileys:
            if smiley.selected:
                pygame.draw.rect(
                    self.screen,
                    (200, 200, 0),
                    smiley.bounding_box())
            smiley.draw(elapsed)
