"""
Sample color picking implementation.
"""

import os
import random
import pygame
from pygame.locals import QUIT
import util
from shader import compile_program

class PickableSmiley(object):

    def __init__(self, screen, pos):
        self.screen = screen
        self.pos = pos
        self.img = pygame.image.load(
            os.path.join('./assets/images/picking', 'smile.png')
        )

    def draw(self, elapsed):
        self.screen.blit(self.img, self.pos)


class ColorPicker(object):

    def __init__(self, screen):
        self.screen = screen
        self.shown = False
        self.background = self._load_img(
            os.path.join('./assets/images/picking', 'ozadje.png')
        )
        self.smileys = [PickableSmiley(screen, (random.randint(100, 600), random.randint(100, 600))) for x in range(5)]

        program = compile_program('''
// Vertex program
varying vec3 pos;
void main() {
    pos = gl_Vertex.xyz;
    gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
}
            ''', '''
// Fragment program
varying vec3 pos;
void main() {
    gl_FragColor.rgb = pos.xyz;
}
            ''')

    def _load_img(self, full_path):
        image = pygame.image.load(full_path)
        return pygame.transform.scale(image, (800, 600))

    def handle_event(self, event):
        if event.type == QUIT:
            util.switch(util.Displays.MENU)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                util.switch(util.Displays.MENU)

    def draw(self, elapsed):
        self.screen.blit(self.background, (0,0))
        for smiley in self.smileys:
            smiley.draw(elapsed)
