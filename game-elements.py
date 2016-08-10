import pygame, sys
import util
from pygame.locals import *

from animation import animate2d, idle, distance
from picking import colorpicker
from tris import tris


# SETTINGS
width, height = 800, 600


def end():
    pygame.quit()
    sys.exit()


class GameElements(object):

    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((width, height), DOUBLEBUF)
        pygame.display.set_caption('game-elements')
        self.menu = Menu(self.screen)
        self.elapsed = 0
        self.clock = pygame.time.Clock()
        self.displays = {}
        self.current_display = self.menu

    def switch_display(self, id):
        self.current_display.show = False
        if id == util.Displays.MENU:
            self.current_display = Menu(self.screen)
        elif id == util.Displays.ANIM2D:
            self.current_display = animate2d.Animation(self.screen)
        elif id == util.Displays.COLORPICKER:
            self.current_display = colorpicker.ColorPicker(self.screen)
        elif id == util.Displays.ANIM_IDLE:
            self.current_display = idle.Animation(self.screen)
        elif id == util.Displays.ANIM_DEPTH:
            self.current_display = distance.Distance(self.screen)
        elif id == util.Displays.TRIS:
            self.current_display = tris.Tris(self.screen)
        self.current_display.show = True

    def loop(self):
        self.elapsed = self.clock.tick(60)
        for event in pygame.event.get():
            if event.type == util.Events.SWITCH:
                self.switch_display(event.screen)
            if self.current_display.show:
                self.current_display.handle_event(event)

        self.screen.fill((20, 20, 20))
        self.current_display.draw(self.elapsed)
        pygame.display.update()
        pygame.display.flip()


class Choice(object):
    def __init__(self, id, name, path, font):
        self.id = id
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
        self.id = util.Displays.MENU
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
            Choice(util.Displays.ANIM2D, '2d animation', None, self._font(40)),
            Choice(util.Displays.COLORPICKER, 'Color picking demo', None, self._font(40)),
            Choice(util.Displays.ANIM_IDLE, '2d idle animation', None, self._font(40)),
            Choice(util.Displays.ANIM_DEPTH, '2d depth-like scene', None, self._font(40)),
            Choice(util.Displays.TRIS, 'Tetris clone', None, self._font(40)),
            Choice(None, 'Quit', None, self._font(40)),
        ]

    def handle_event(self, event):
        if event.type == QUIT:
            end()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                end()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.next()
            elif event.key == pygame.K_UP:
                self.previous()
            elif event.key == pygame.K_RETURN:
                if self.selected_index == len(self.choices) - 1:
                    pygame.quit()
                    sys.exit()
                else:
                    util.switch(self.choices[self.selected_index].id)

    def next(self):
        self.selected_index = (self.selected_index + 1) % len(self.choices)

    def previous(self):
        self.selected_index = (self.selected_index - 1) % len(self.choices)

    def draw(self, elapsed):
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
