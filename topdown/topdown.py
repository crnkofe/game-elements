"""
Sample top down zelda-like mini game
"""

import os
import random
import pygame
import collections
from pygame.locals import QUIT
import pc
import util


Point = collections.namedtuple('Point', ['x', 'y'])
Size = collections.namedtuple('Size', ['w', 'h'])


class Area(object):
    """
    Rectangular set of tiles
    """

    def __init__(self, screen, size, walls=0):
        self.screen = screen
        self.area = {}
        self.size = size
        info = pygame.display.Info()
        self.window_size = Size(info.current_w, info.current_h)
        for row_idx in range(size.h):
            self.area[row_idx] = {}
            for col_idx in range(size.w):
                if col_idx == 0 or col_idx == (size.w - 1):
                    self.area[row_idx][col_idx] = Wall(Point(row_idx, col_idx))
                elif row_idx == 0 or row_idx == (size.h - 1):
                    self.area[row_idx][col_idx] = Wall(Point(row_idx, col_idx))
                else:
                    self.area[row_idx][col_idx] = Tile(Point(row_idx, col_idx))

    def eff_size(self):
        return Size(self.window_size.w * 0.7, self.window_size.h * 0.9)

    def eff_block(self):
        effw, effh = self.eff_size().w, self.eff_size().h
        return Size(
            (effw / self.size.w),
            (effh / self.size.h)
        )

    def bottom_left(self):
        effsize = self.eff_size()
        return Point(self.window_size.w / 2 - effsize.w / 2, self.window_size.h / 2 - effsize.h / 2)


    def draw(self):
        effblock = self.eff_block()
        bl = self.bottom_left()

        for row_idx in range(self.size.h):
            for col_idx in range(self.size.w):
                self.area[row_idx][col_idx].draw(
                    self.screen,
                    Point(
                        bl.x + col_idx * effblock.w,
                        bl.y + row_idx * effblock.h
                    ),
                    Size(
                        effblock.w * 0.9,
                        effblock.h * 0.9
                    )
                )

class Tile(object):
    def __init__(self, loc):
        self.loc = loc

    def draw(self, screen, offset, size):
        pygame.draw.rect(
            screen,
            (20, 150, 20),
            (offset.x, offset.y, size.w, size.h)
        )


class Wall(Tile):
    def __init__(self, loc):
        super(Wall, self).__init__(loc)

    def draw(self, screen, offset, size):
        pygame.draw.rect(
            screen,
            (120, 120, 120),
            (offset.x, offset.y, size.w, size.h)
        )


class TopDown(object):

    def __init__(self, screen):
        self.screen = screen
        self.shown = False
        self.areas = {
            "left": Area(screen, Size(10, 10)),
            "bot": Area(screen, Size(10, 10)),
            "center": Area(screen, Size(20, 20)),
            "right": Area(screen, Size(10, 10)),
            "top": Area(screen, Size(10, 10)),
        }
        self.pc = pc.Player(Point(10, 10))
        self.current_area = "center"

    def handle_event(self, event):
        if event.type == QUIT:
            util.switch(util.Displays.MENU)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                util.switch(util.Displays.MENU)

    def area(self):
        return self.areas[self.current_area]

    def draw_area(self):
        self.area().draw()

    def draw(self, elapsed):
        self.draw_area()
        self.pc.draw(self.screen, self.area().bottom_left(), self.area().eff_block())
