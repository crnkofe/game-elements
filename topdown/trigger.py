def callback():
    pass


class MapTrigger(object):

    def __init__(self, loc, enter=callback, exit=callback):
        self.loc = loc
        self.enter = enter
        self.exit = exit

    def enter(self):
        self.enter()

    def exit(self):
        self.exit()


class Toggle(object):

    def __init__(self, tiles):
        self.tiles = tiles

    def toggle(self):
        for tile in self.tiles:
            tile.toggle()
