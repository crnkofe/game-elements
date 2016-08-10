import pygame


class Events(object):
    SWITCH = pygame.USEREVENT + 0


class Displays(object):
    MENU = 1
    ANIM2D = 2
    COLORPICKER = 3
    ANIM_IDLE = 4
    ANIM_DEPTH = 5
    TRIS = 6


def switch(screen_name):
    evt = pygame.event.Event(
        Events.SWITCH, {"screen": screen_name})
    pygame.event.post(evt)
