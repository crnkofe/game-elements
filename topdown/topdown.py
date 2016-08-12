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
                    self.area[row_idx][col_idx] = Wall(Point(col_idx, row_idx))
                elif row_idx == 0 or row_idx == (size.h - 1):
                    self.area[row_idx][col_idx] = Wall(Point(col_idx, row_idx))
                else:
                    self.area[row_idx][col_idx] = Tile(Point(col_idx, row_idx))

    def make_doors(self, from_loc, to_loc):
        for x in range(from_loc.x, to_loc.x + 1):
            for y in range(from_loc.y, to_loc.y + 1):
                self.area[y][x] = Door(Point(x, y))

    def passable(self, pos):
        if not pos.y in self.area:
            return False
        if not pos.x in self.area[pos.y]:
            return False
        return self.area[pos.y][pos.x].passable()

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

    def passable(self):
        return True


class Wall(Tile):
    def __init__(self, loc):
        super(Wall, self).__init__(loc)

    def draw(self, screen, offset, size):
        pygame.draw.rect(
            screen,
            (120, 120, 120),
            (offset.x, offset.y, size.w, size.h)
        )

    def passable(self):
        return False


class Door(Tile):

    def __init__(self, loc):
        super(Door, self).__init__(loc)
        self.opened = False

    def draw(self, screen, offset, size):
        if self.passable():
            color = (120, 120, 120)
        else:
            color = (192, 127, 0)
        pygame.draw.rect(
            screen, color,
            (offset.x, offset.y, size.w, size.h)
        )

    def passable(self):
        return self.opened


class TopDown(object):

    def __init__(self, screen):
        self.screen = screen
        self.shown = False
        self.areas = {
            "left": self.left_area(),
            "bot": self.bot_area(),
            "center": self.central_area(),
            "right": self.right_area(),
            "top": self.top_area(),
        }
        self.pc = pc.Player(Point(10, 10))
        self.current_area = "center"

    def left_area(self):
        ret = Area(self.screen, Size(10, 10))
        ret.make_doors(Point(9, 3), Point(9, 6))
        return ret

    def right_area(self):
        ret = Area(self.screen, Size(10, 10))
        ret.make_doors(Point(0, 3), Point(0, 6))
        return ret

    def bot_area(self):
        ret = Area(self.screen, Size(10, 10))
        ret.make_doors(Point(3, 0), Point(6, 0))
        return ret

    def top_area(self):
        ret = Area(self.screen, Size(10, 10))
        ret.make_doors(Point(3, 9), Point(6, 9))
        return ret

    def central_area(self):
        ret = Area(self.screen, Size(20, 20))
        ret.make_doors(Point(8, 0), Point(11, 0))
        ret.make_doors(Point(8, 19), Point(11, 19))
        ret.make_doors(Point(0, 8), Point(0, 11))
        ret.make_doors(Point(19, 8), Point(19, 11))
        return ret

    def handle_event(self, event):
        if event.type == QUIT:
            util.switch(util.Displays.MENU)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                util.switch(util.Displays.MENU)

            if event.key == pygame.K_LEFT:
                self.pc.move(-1, 0)
            if event.key == pygame.K_RIGHT:
                self.pc.move(1, 0)
            if event.key == pygame.K_DOWN:
                self.pc.move(0, 1)
            if event.key == pygame.K_UP:
                self.pc.move(0, -1)

            if not self.area().passable(self.pc.pos) or\
                    self.pc.out_of_bounds(self.area()):
                self.pc.reset()

    def area(self):
        return self.areas[self.current_area]

    def draw_area(self):
        self.area().draw()

    def draw(self, elapsed):
        self.draw_area()
        self.pc.draw(self.screen, self.area().bottom_left(), self.area().eff_block())
