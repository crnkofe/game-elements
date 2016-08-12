import collections

Point = collections.namedtuple('Point', ['x', 'y'])


class AreaTransition(object):

    def __init__(self, area1, area2, direction):
        self.area1 = area1
        self.area2 = area2
        self.direction = direction
        self.reset()

    def reset(self):
        self.finished = False
        # total elapsed since beginning of animation
        self.total_elapsed = 0
        # animation length in ms
        self.length = 1000

    def draw(self, elapsed):
        if self.total_elapsed > self.length:
            self.finished = True
            return
        self.total_elapsed += elapsed
        percent_elapsed = float(self.total_elapsed) / self.length

        ar1_sz = self.area1.eff_size()
        self.area1.draw(offset=Point(ar1_sz.w * percent_elapsed, 0))
