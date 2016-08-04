"""
Sample idle 2d animation from a set of images
"""

import math
import os.path
import pygame
from pygame.locals import QUIT
import util


class Movement(object):
    IDLE = 0
    LEFT = 1
    TOP = 2
    RIGHT = 3
    DOWN = 4


class Sequence(object):

    def __init__(self, files, animation_length=None, directory="./assets/images/n1"):
        self.images = [
            self._load_transform(os.path.join(directory, filename))
            for filename in files]
        self.animation_progress = 0
        self.total_animation_length = animation_length or float(len(self.images)) / 4

    def reset(self):
        self.animation_progress = 0

    def _load_transform(self, full_path):
        image = pygame.image.load(full_path)
        return pygame.transform.scale(image, (800, 600))

    def draw(self, screen, elapsed):
        self.animation_progress = (self.animation_progress + elapsed) % \
            (self.total_animation_length * 1000)
        current_image_index = int(math.floor(
            len(self.images) * float(self.animation_progress) / (self.total_animation_length * 1000)))
        screen.blit(self.images[current_image_index], (0,0))


class Animation(object):

    def __init__(self, screen):
        self.screen = screen
        files_idle = [
            "n1_0.png",
            "n1_1.png",
            "n1_2.png",
            "n1_3.png",
        ]
        files_left = [
            "n1-l_0.png",
            "n1-l_1.png",
        ]
        files_right = [
            "n1-r_0.png",
            "n1-r_1.png",
        ]
        self.sequences = {
            Movement.IDLE: Sequence(files_idle),
            Movement.LEFT: Sequence(files_left),
            Movement.TOP: Sequence(files_idle),
            Movement.RIGHT: Sequence(files_right),
            Movement.DOWN: Sequence(files_idle),
        }

        self.current_sequence = self.sequences[Movement.IDLE]
        self.shown = False
        self.key_pressed = False
        self.return_to_idle = 1 * 1000
        self.elapsed_since_change = 0

    def _load_transform(self, full_path):
        image = pygame.image.load(full_path)
        return pygame.transform.scale(image, (800, 600))

    def _map_to_sequence(self, event):
        if event.key == pygame.K_LEFT:
            return self.sequences[Movement.LEFT]
        elif event.key == pygame.K_UP:
            return self.sequences[Movement.TOP]
        elif event.key == pygame.K_RIGHT:
            return self.sequences[Movement.RIGHT]
        elif event.key == pygame.K_DOWN:
            return self.sequences[Movement.DOWN]
        return None

    def handle_event(self, event):
        self.key_pressed = False
        if event.type == QUIT:
            util.switch(util.Displays.MENU)
        if event.type == pygame.KEYDOWN:
            previous_sequence = self.current_sequence

            if event.key == pygame.K_ESCAPE:
                util.switch(util.Displays.MENU)

            if event.key in (pygame.K_LEFT,
                             pygame.K_UP,
                             pygame.K_RIGHT,
                             pygame.K_DOWN):
                self.key_pressed = True
                self.elapsed_since_change = 0
                self.current_sequence = self._map_to_sequence(event)
                if previous_sequence != self.current_sequence:
                    self.current_sequence.reset()
        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT,
                             pygame.K_UP,
                             pygame.K_RIGHT,
                             pygame.K_DOWN):
                self.current_sequence = self.sequences[Movement.IDLE]
                self.current_sequence.reset()

    def draw(self, elapsed):
        idle = self.current_sequence == self.sequences[Movement.IDLE]
        actual_elapsed = elapsed
        if not self.key_pressed and not idle:
            actual_elapsed = 0
        self.current_sequence.draw(self.screen, actual_elapsed)
