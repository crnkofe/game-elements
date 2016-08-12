

class AreaTransition(object):

    def __init__(self, area1, area2, direction):
        self.area1 = area1
        self.area2 = area2
        self.direction = direction
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
