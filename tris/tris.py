"""
Sample Tetris clone
"""

import math
import os.path
import collections
import pygame
from pygame.locals import QUIT
import util


Point = collections.namedtuple('Point', ['x', 'y'])


class TrisBlockState(object):
    EMPTY = 0
    FULL = 1


class TrisBlock(object):

    def __init__(self, area_width, area_height):
        self.blocks = [Point(-1, 0), Point(0, 0), Point(1, 0), Point(2, 0)]
        self.pos = Point(area_width / 2, area_height - 1)

    def pos_blocks(self):
        return [Point(p.x + self.pos.x, p.y + self.pos.y) for p in self.blocks]


class Tris(object):

    def __init__(self, screen):
        self.screen = screen

        info = pygame.display.Info()
        self.size = (info.current_w, info.current_h)

        # area goes from 0 to n where lower is bottom on the screen
        self.area_width = 8
        self.area_height = 10
        self.area = {i: [TrisBlockState.EMPTY for j in range(self.area_width)] for i in range(self.area_height)}
        self.block = None
        self.score = 0
        self.current_block = TrisBlock(self.area_width, self.area_height)

    def handle_event(self, event):
        if event.type == QUIT:
            util.switch(util.Displays.MENU)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                util.switch(util.Displays.MENU)
            if event.key == pygame.K_LEFT:
                pass
            if event.key == pygame.K_RIGHT:
                pass
            if event.key == pygame.K_SPACE:
                pass

    def draw_area(self):
        w, h = self.size
        effw = w * 0.6
        effh = h * 0.9
        bl = Point(w / 2 - effw / 2, h / 2 - effh / 2)
        pygame.draw.rect(
            self.screen,
            (120, 120, 120),
            (bl.x, bl.y,
             effw, effh),
            )

        blwidth = float(effw) / self.area_width
        blheight = float(effh) / self.area_height

        for row_idx in range(self.area_height):
            for col_idx in range(self.area_width):
                if self.area[row_idx][col_idx] == TrisBlockState.FULL:
                    point = Point(bl.x + (self.area_height - col_idx - 1) * blwidth,
                                  bl.y + row_idx * blheight)
                    pygame.draw.rect(
                        self.screen,
                        (200, 200, 200),
                        (point.x, point.y, blwidth, blheight))


        for block in self.current_block.pos_blocks():
            point = Point(bl.x + block.x * blwidth,
                          bl.y + (self.area_height - block.y - 1) * blheight)
            pygame.draw.rect(
                self.screen,
                (200, 200, 200),
                (point.x, point.y, blwidth, blheight))

    def draw(self, elapsed):
        self.draw_area()
