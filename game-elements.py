import pygame, sys
from pygame.locals import *

# SETTINGS
width, height = 800, 600


class GameElements(object):

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('game-elements')
        self.menu = Menu(self.screen)

    def loop(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            if self.menu.show:
                self.menu.handle_event(event)

        self.screen.fill((20, 20, 20))
        self.menu.draw()
        pygame.display.update()


class Choice(object):
    def __init__(self, name, path, font):
        self.name = name
        self.path = path
        self.font = font
        self.color = None

    def render(self, color):
        if not self.color or color != self.color:
            self.label = self.font.render(self.name, 1, color)
        return self.font.size(self.name)


class Menu(object):

    def __init__(self, screen):
        self.screen = screen
        self.fonts = {}
        self.title_text = '*** Game Elements ***'
        self.title = self._font(40).render(self.title_text, 1, (240, 240, 240))
        self.show = True
        self.choices = self._choices()
        self.selected_index = 0

    def _font(self, size):
        if size in self.fonts:
            return self.fonts[size]

        self.fonts[size] = pygame.font.SysFont(
            "/usr/share/fonts/truetype/droid/DroidSansMono.ttf",
            size)
        return self.fonts[size]

    def _choices(self):
        return [
            Choice('2d idle animation', None, self._font(40)),
            Choice('Quit', None, self._font(40)),
        ]

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.next()
            elif event.key == pygame.K_UP:
                self.previous()
            elif event.key == pygame.K_RETURN:
                if self.selected_index == len(self.choices) - 1:
                    pygame.quit()
                    sys.exit()

    def next(self):
        self.selected_index = (self.selected_index + 1) % len(self.choices)

    def previous(self):
        self.selected_index = (self.selected_index - 1) % len(self.choices)

    def draw(self):
        title_width, title_height = self._font(40).size(self.title_text)
        self.screen.blit(self.title, (width / 2 - title_width / 2, 100))

        choice_height = 20
        offset = 300
        for idx, choice in enumerate(self.choices):
            if idx == self.selected_index:
                choice_width, choice_height = choice.render((220, 220, 220))
            else:
                choice_width, choice_height = choice.render((0, 0, 180))

            location = (width / 2 - choice_width / 2, offset + idx * choice_height)
            self.screen.blit(choice.label, location)


elements = GameElements()
while True:
    elements.loop()
