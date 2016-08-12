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


class ShowTransition(MapTrigger):

    def __init__(self, loc, game, to, storyboard):
        super(ShowTransition, self).__init__(loc, self.enter)
        self.game = game
        self.to = to
        self.storyboard = storyboard

    def enter(self):
        self.game.storyboard_stack.append(self.storyboard)
        self.game.current_area = self.to


class Toggle(object):

    def __init__(self, tiles):
        self.tiles = tiles

    def toggle(self):
        for tile in self.tiles:
            tile.toggle()
