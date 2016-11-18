'''
'''

import pygame
from random import randint

class SimpleExplosion(pygame.sprite.Sprite):
    clear = (0, 0, 0)
    def __init__(self, xy, radius, color=(255, 0, 0), speed=10, layer=0, generation=4):
        super().__init__()

        self.xy = xy
        self.maxRadius = radius
        self.radius = 1
        self.fgcolor = color
        self.speed = speed
        self.layer = layer
        self.generation = generation
        
        self.image = pygame.Surface((radius*2,radius*2), 32)
        self.rect = self.image.get_rect(center=xy)
        self.image.set_colorkey(self.clear)

    @property
    def new_xy(self):
        x,y = map(int,self.xy)
        x = randint(x-self.maxRadius,x+self.maxRadius)
        y = randint(y-self.maxRadius,y+self.maxRadius)
        return x,y

    def update(self, dt):
        '''
        '''

        if self.alive():
            if self.radius > self.maxRadius:
                if self.generation > 0:
                    e = SimpleExplosion(self.new_xy,
                                        self.radius,
                                        self.fgcolor,
                                        self.speed + 5,
                                        self.layer,
                                        self.generation - 1)
                    e.add(self.groups())
                self.kill()
            self.render()
            self.radius += int(self.maxRadius * (self.speed / 100.))

    def render(self):
        rect = self.image.get_rect()
        self.image.fill(self.clear)
        pygame.draw.circle(self.image, self.fgcolor, rect.center , self.radius)
        pygame.draw.circle(self.image, self.clear, rect.center , max(self.radius-2,1))        
        

