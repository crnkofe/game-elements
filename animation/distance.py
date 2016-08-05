"""
Distance simulation using black and white image as depth map.
"""

import os.path
import pygame
from pygame.locals import QUIT
import util


class Distance(object):

    def __init__(self, screen):
        self.screen = screen
        directory = "./assets/images/mask"
        self.background_file = "ozadje-0.png"
        self.background_depth_file = "ozadje-1.png"
        self.image_file = "./assets/images/nyan/nyan00.png"

        self.background = self._load_transform(
            os.path.join(directory, self.background_file)
        )
        self.background_depth = self._load_transform(
            os.path.join(directory, self.background_depth_file)
        )

        self.image = self._load_transform(self.image_file, (140, 100))

        self.image_loc = None
        self.image_color = None
        self.shown = False
        self.key_pressed = False
        self.return_to_idle = 1 * 1000
        self.elapsed_since_change = 0

    def _load_transform(self, full_path, custom_transform=(800, 600)):
        image = pygame.image.load(full_path)
        return pygame.transform.scale(image, custom_transform)

    def handle_event(self, event):
        self.key_pressed = False
        if event.type == QUIT:
            util.switch(util.Displays.MENU)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                util.switch(util.Displays.MENU)
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            self.image_loc = pos
            self.image_color = self.background_depth.get_at(pos)

    def draw(self, elapsed):
        self.screen.blit(self.background, (0,0))
        if self.image_loc:
            actual_ratio = (sum(self.image_color) - 255) / (3 * 255.0) * 2
            ratio = max(0.1, actual_ratio)
            if ratio > 0.1:
                w, h = int(200 * ratio), int(100 * ratio)
                new_surface = pygame.transform.scale(self.image, (w, h))
                self.screen.blit(new_surface, (self.image_loc[0] - w/2, self.image_loc[1] - h/2))
