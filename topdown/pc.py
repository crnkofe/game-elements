import pygame
import collections

Point = collections.namedtuple('Point', ['x', 'y'])
Size = collections.namedtuple('Size', ['w', 'h'])


class Player(object):

    def __init__(self, pos):
        self.previous = None
        self.pos = pos

    def draw(self, screen, bl, effblock):
        pygame.draw.rect(
            screen,
            (250, 250, 250),
            (bl.x + self.pos.x * effblock.w,
             bl.y + self.pos.y * effblock.h,
             effblock.w * 0.9,
             effblock.h * 0.9)
        )

    def move(self, x, y):
        self.previous = self.pos
        self.pos = Point(self.pos.x + x, self.pos.y + y)

    def out_of_bounds(self, area):
        if self.pos.x < 0 or self.pos.x >= area.size.w:
            return True
        if self.pos.y < 0 or self.pos.y >= area.size.h:
            return True
        return False

    def reset(self):
        self.pos = self.previous
        self.previous = None
