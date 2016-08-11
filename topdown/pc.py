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
            (bl.x + self.pos.y * effblock.w,
             bl.y + self.pos.x * effblock.h,
             effblock.w * 0.9,
             effblock.h * 0.9)
        )

    def move(self, x, y):
        self.previous = self.pos
        self.pos = Point(x, y)

    def out_of_bounds(self, area):
        if self.pos.x < 0 or self.pos.x >= area.size.width:
            return True
        if self.pos.y < 0 or self.pos.y >= area.size.height:
            return True
        return False

    def reset(self):
        self.pos = self.previous
        self.previous = None
