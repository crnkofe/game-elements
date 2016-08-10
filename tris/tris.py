"""
Sample Tetris clone
"""

import random
import collections
import pygame
from pygame.locals import QUIT
import util


Point = collections.namedtuple('Point', ['x', 'y'])


class TrisBlockState(object):
    EMPTY = 0
    FULL = 1


class TrisState(object):
    RUNNING = 0
    OVER = 1


def generate_block(area_width, area_height):
    return random.choice(
        (
            LineBlock(area_width, area_height),
            SquareBlock(area_width, area_height),
            LBlock(area_width, area_height),
            ReverseLBlock(area_width, area_height),
            SBlock(area_width, area_height),
        )
    )

class BaseBlock(object):

    def __init__(self, area_width, area_height, blocks):
        self.blocks = blocks
        self.previous_pos = None
        max_y = max(b.y for b in blocks)
        self.pos = Point(area_width / 2, area_height - (max_y + 1))

    def pos_blocks(self):
        if not self.blocks:
            return []
        if not self.pos:
            return []
        return [Point(p.x + self.pos.x, p.y + self.pos.y) for p in self.blocks]

    def move_left(self):
        self.previous_pos = self.pos
        self.pos = Point(self.pos.x - 1, self.pos.y)

    def move_right(self):
        self.previous_pos = self.pos
        self.pos = Point(self.pos.x + 1, self.pos.y)

    def move_down(self):
        self.previous_pos = self.pos
        self.pos = Point(self.pos.x, self.pos.y - 1)

    def reset(self):
        self.pos = self.previous_pos
        self.previous_pos = None


class LineBlock(BaseBlock):
    def __init__(self, area_width, area_height):
        blocks = [(-1, 0), (0, 0), (1, 0), (2, 0)]
        super(LineBlock, self).__init__(
            area_width, area_height,
            map(lambda p: Point(p[0], p[1]), blocks))


class SquareBlock(BaseBlock):
    def __init__(self, area_width, area_height):
        blocks = [(0, 0), (1, 0), (0, -1), (1, -1)]
        super(SquareBlock, self).__init__(
            area_width, area_height,
            map(lambda p: Point(p[0], p[1]), blocks))


class LBlock(BaseBlock):
    def __init__(self, area_width, area_height):
        blocks = [(0, 1), (0, 0), (1, 0), (2, 0)]
        super(LBlock, self).__init__(
            area_width, area_height,
            map(lambda p: Point(p[0], p[1]), blocks))


class ReverseLBlock(BaseBlock):
    def __init__(self, area_width, area_height):
        blocks = [(0, -1), (0, 0), (1, 0), (2, 0)]
        super(ReverseLBlock, self).__init__(
            area_width, area_height,
            map(lambda p: Point(p[0], p[1]), blocks))


class SBlock(BaseBlock):
    def __init__(self, area_width, area_height):
        blocks = [(0, 1), (-1, 0), (0, -1), (-1, -2)]
        super(SBlock, self).__init__(
            area_width, area_height,
            map(lambda p: Point(p[0], p[1]), blocks))


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
        self.state = TrisState.RUNNING
        self.current_block = generate_block(self.area_width, self.area_height)
        self.fonts = {}

        self.elapsed_counter = 0
        self.falling_speed = 1
        self.lines_cleared = 0

        self.over_text = self._font(40).render("GAME OVER!", 1, (240, 10, 10))

    def _font(self, size):
        if size in self.fonts:
            return self.fonts[size]

        self.fonts[size] = pygame.font.SysFont(
            "/usr/share/fonts/truetype/droid/DroidSansMono.ttf",
            size)
        return self.fonts[size]

    def handle_event(self, event):
        if event.type == QUIT:
            util.switch(util.Displays.MENU)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                util.switch(util.Displays.MENU)
            if event.key == pygame.K_LEFT:
                self.current_block.move_left()
                if self.over_edge():
                    self.current_block.reset()
            if event.key == pygame.K_RIGHT:
                self.current_block.move_right()
                if self.over_edge():
                    self.current_block.reset()
            if event.key == pygame.K_DOWN:
                self.current_block.move_down()
                if self.over_edge():
                    self.current_block.reset()
            if event.key == pygame.K_SPACE:
                pass

            self.check_collision()

    def check_collision(self):
        if self.collision():
            self.current_block.reset()

            if self.collision():
                self.state = TrisState.OVER
                return

            eff_blocks = self.current_block.pos_blocks()
            for block in eff_blocks:
                if block.y in self.area:
                    if block.x < len(self.area[block.y]):
                        self.area[block.y][block.x] = TrisBlockState.FULL

            self.current_block = generate_block(self.area_width, self.area_height)
            if self.collision():
                self.state = TrisState.OVER
                return


    def over_edge(self):
        if not self.current_block:
            return False
        eff_blocks = self.current_block.pos_blocks()
        if any([block.x < 0 or block.x >= self.area_width for block in eff_blocks]):
            return True
        return False

    def collision(self):
        if not self.current_block:
            return False
        eff_blocks = self.current_block.pos_blocks()
        if any([block.y < 0 for block in eff_blocks]):
            return True
        if any([self.area[block.y][block.x] == TrisBlockState.FULL for block in eff_blocks]):
            return True
        return False

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
                    point = Point(bl.x + col_idx * blwidth,
                                  bl.y + (self.area_height - row_idx - 1) * blheight)
                    pygame.draw.rect(
                        self.screen,
                        (200, 200, 200),
                        (point.x, point.y, blwidth, blheight))

        for block in self.current_block.pos_blocks():
            point = Point(bl.x + block.x * blwidth,
                          bl.y + (self.area_height - block.y - 1) * blheight)
            pygame.draw.rect(
                self.screen,
                (0, 50, 180),
                (point.x, point.y, blwidth, blheight))

    def draw(self, elapsed):
        self.elapsed_counter += elapsed
        if self.elapsed_counter > self.falling_speed * 1000:
            self.elapsed_counter -= 1000

            self.current_block.move_down()
            if self.over_edge():
                self.current_block.reset()
            self.check_collision()


        if self.state == TrisState.RUNNING:
            self.draw_area()
        elif self.state == TrisState.OVER:
            width, height = self.size
            over_width, over_height = self._font(40).size("GAME OVER!")
            location = (width / 2 - over_width / 2, height / 2 - over_height / 2)
            self.screen.blit(self.over_text, location)
