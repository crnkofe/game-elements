"""
Sample 2d animation from a set of images
"""

import math
import os.path
import pygame
from pygame.locals import QUIT
import util


class Animation(object):

    def __init__(self, screen):
        self.screen = screen
        directory = "./assets/images/nyan"
        files = [
            "nyan00.png",
            "nyan01.png",
            "nyan02.png",
            "nyan03.png",
            "nyan04.png",
            "nyan05.png",
            "nyan06.png",
            "nyan07.png",
            "nyan08.png",
            "nyan09.png",
            "nyan10.png",
            "nyan11.png",
        ]

        self.images = [
            self._load_transform(os.path.join(directory, filename))
            for filename in files]

        self.animation_progress = 0
        self.total_animation_length = 1 #  in seconds
        self.files = []
        self.shown = False


    def _load_transform(self, full_path):
        image = pygame.image.load(full_path)
        return pygame.transform.scale(image, (800, 600))

    def handle_event(self, event):
        if event.type == QUIT:
            util.switch(util.Displays.MENU)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
               util.switch(util.Displays.MENU)

    def draw(self, elapsed):
        self.animation_progress = (self.animation_progress + elapsed) % \
            (self.total_animation_length * 1000)
        current_image_index = int(math.floor(
            len(self.images) * float(self.animation_progress) / (self.total_animation_length * 1000)))
        self.screen.blit(self.images[current_image_index], (0,0))
