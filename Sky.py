'''
'''

import pygame

from random import randint, choice

class Star(pygame.sprite.Sprite):
    bgcolor = (0,0,0)
    fgcolor = (255,255,255)
    colors = [(255,0,0), (0,255,0), (0,0,255)]

    def __init__(self, xy):
        super().__init__()
        self.image = pygame.Surface((3,3), depth=32)
        self.rect = self.image.get_rect()
        self.rect.center = xy
        self.render(self.colors[0])
        self.twinkleInterval = randint(500, 3000)
        self.twinkle = 0
        
    def update(self, time):

        self.twinkle -= 1
        self.render(doTwinkle=(self.twinkle<=10))
        if self.twinkle <= 0:
            self.twinkle = self.twinkleInterval

    def render(self, color=(255,255,255), doTwinkle=False):

        if doTwinkle:
            self.image.fill(self.bgcolor)
            r = self.image.get_rect()
            c = choice(self.colors)
            pygame.draw.line(self.image, c, r.midtop, r.midbottom)
            pygame.draw.line(self.image, c, r.midleft, r.midright)
        else:
            self.image.fill(color)
        
