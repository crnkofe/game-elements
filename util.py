import pygame


class Events(object):
    SWITCH = pygame.USEREVENT + 0


class Displays(object):
    MENU = 1
    ANIM2D = 2
    COLORPICKER = 3


def switch(screen_name):
    evt = pygame.event.Event(
        Events.SWITCH, {"screen": screen_name})
    pygame.event.post(evt)
