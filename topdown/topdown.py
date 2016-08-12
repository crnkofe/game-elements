"""
Sample top down zelda-like mini game
"""

import pygame
import collections
from pygame.locals import QUIT
import pc
import trigger
import storyboard
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
        self.doors = collections.defaultdict()
        info = pygame.display.Info()
        self.window_size = Size(info.current_w, info.current_h)
        self.triggers = {}
        for row_idx in range(size.h):
            self.area[row_idx] = {}
            for col_idx in range(size.w):
                if col_idx == 0 or col_idx == (size.w - 1):
                    self.area[row_idx][col_idx] = Wall(Point(col_idx, row_idx))
                elif row_idx == 0 or row_idx == (size.h - 1):
                    self.area[row_idx][col_idx] = Wall(Point(col_idx, row_idx))
                else:
                    self.area[row_idx][col_idx] = Tile(Point(col_idx, row_idx))

    def make_door(self, from_loc, to_loc, from_dest_loc, name, opened=False):
        door_tiles = []
        for x in range(from_loc.x, to_loc.x + 1):
            for y in range(from_loc.y, to_loc.y + 1):
                door = Door(Point(x, y), opened=opened)
                door.dest_loc = Point(
                    from_dest_loc.x + (x - from_loc.x),
                    from_dest_loc.y + (y - from_loc.y)
                )
                door_tiles.append(door)
                self.area[y][x] = door
        self.doors[name] = door_tiles

    def add_trigger(self, loc, trigger):
        if loc not in self.triggers:
            self.triggers[loc] = []

        self.triggers[loc].append(trigger)

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
        return Point(
            self.window_size.w / 2 - effsize.w / 2,
            self.window_size.h / 2 - effsize.h / 2)

    def draw(self, offset=Point(0, 0), limit_bl=None, limit_tr=None):
        effblock = self.eff_block()
        bl = self.bottom_left()

        for row_idx in range(self.size.h):
            for col_idx in range(self.size.w):
                pt = Point(
                    bl.x + col_idx * effblock.w,
                    bl.y + row_idx * effblock.h
                )
                sz = Size(
                    effblock.w * 0.9,
                    effblock.h * 0.9
                )

                if limit_bl:
                    if pt.x < limit_bl.x:
                        continue
                    if pt.y < limit_bl.y:
                        continue
                if limit_tr:
                    if (pt.x + sz.w) > limit_tr.x:
                        continue
                    if (pt.y + sz.h) > limit_tr.y:
                        continue

                offpt = Point(pt.x + offset.x, pt.y + offset.y)

                self.area[row_idx][col_idx].draw(
                    self.screen, offpt, sz
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

    def __init__(self, loc, opened=False):
        super(Door, self).__init__(loc)
        self.opened = opened

    def draw(self, screen, offset, size):
        if self.passable():
            color = (20, 150, 20)
        else:
            color = (192, 127, 0)
        pygame.draw.rect(
            screen, color,
            (offset.x, offset.y, size.w, size.h)
        )

    def toggle(self):
        self.opened = not self.opened

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

        self.add_triggers()
        self.pc = pc.Player(Point(10, 10))
        self.current_area = "center"
        self.storyboard_stack = []

    def left_area(self):
        ret = Area(self.screen, Size(10, 10))
        ret.make_door(Point(9, 3), Point(9, 6), Point(0, 8),  "center", opened=True)
        return ret

    def right_area(self):
        ret = Area(self.screen, Size(10, 10))
        ret.make_door(Point(0, 3), Point(0, 6), Point(19, 8), "center")
        return ret

    def bot_area(self):
        ret = Area(self.screen, Size(10, 10))
        ret.make_door(Point(3, 0), Point(6, 0), Point(8, 19), "center")
        return ret

    def top_area(self):
        ret = Area(self.screen, Size(10, 10))
        ret.make_door(Point(3, 9), Point(6, 9), Point(8, 0), "center")
        return ret

    def central_area(self):
        ret = Area(self.screen, Size(20, 20))
        ret.make_door(Point(8, 0), Point(11, 0), Point(3, 0), "top")
        ret.make_door(Point(8, 19), Point(11, 19), Point(3, 9), "bottom")
        ret.make_door(Point(0, 8), Point(0, 11), Point(9, 3), "left")
        ret.make_door(Point(19, 8), Point(19, 11), Point(0, 3), "right")
        return ret

    def add_triggers(self):
        center = self.areas['center']
        left = self.areas['left']
        for door in center.doors['left']:
            center.add_trigger(door.loc,
                trigger.ShowTransition(
                    door.loc,
                    self,
                    "left",
                    storyboard.AreaTransition(
                        center,
                        self.areas['left'],
                        Point(-1, 0)
                    )
                )
            )
        for door in left.doors['center']:
            left.add_trigger(door.loc,
                trigger.ShowTransition(
                    door.loc,
                    self,
                    "center",
                    storyboard.AreaTransition(
                        left,
                        self.areas['center'],
                        Point(1, 0)
                    )
                )
            )
        center.add_trigger(Point(8, 9),
            trigger.MapTrigger(
                Point(8, 9),
                trigger.Toggle(center.doors['left']).toggle
            )
        )
        center.add_trigger(Point(12, 11),
            trigger.MapTrigger(
                Point(12, 11),
                trigger.Toggle(center.doors['right']).toggle
            )
        )

    def handle_event(self, event):
        if event.type == QUIT:
            util.switch(util.Displays.MENU)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                util.switch(util.Displays.MENU)

            if len(self.storyboard_stack) > 0:
                return

            previous = self.pc.pos

            if event.key == pygame.K_LEFT:
                self.pc.move(-1, 0)
            if event.key == pygame.K_RIGHT:
                self.pc.move(1, 0)
            if event.key == pygame.K_DOWN:
                self.pc.move(0, 1)
            if event.key == pygame.K_UP:
                self.pc.move(0, -1)

            if event.key in (pygame.K_LEFT,
                             pygame.K_RIGHT,
                             pygame.K_DOWN,
                             pygame.K_UP):
                if not self.area().passable(self.pc.pos) or\
                        self.pc.out_of_bounds(self.area()):
                    self.pc.reset()
                else:
                    for trig in self.area().triggers.get(previous, []):
                        trig.exit()
                    for trig in self.area().triggers.get(self.pc.pos, []):
                        trig.enter()

    def area(self):
        return self.areas[self.current_area]

    def draw_area(self):
        self.area().draw()

    def draw(self, elapsed):
        if len(self.storyboard_stack) > 0:
            if self.storyboard_stack[-1].finished:
                last = self.storyboard_stack.pop()
                last.reset()
            else:
                self.storyboard_stack[-1].draw(elapsed)
                return

        self.draw_area()
        self.pc.draw(
            self.screen,
            self.area().bottom_left(),
            self.area().eff_block()
        )

        bl = self.area().bottom_left()
        effblock = self.area().eff_block()
        for loc, trig in self.area().triggers.iteritems():
            offset = Point(
                bl.x + loc.x * effblock.w,
                bl.y + loc.y * effblock.h
            )
            size = Size(
                effblock.w * 0.5,
                effblock.h * 0.5
            )
            pygame.draw.rect(
                self.screen,
                (150, 20, 20),
                (offset.x, offset.y, size.w, size.h)
            )
