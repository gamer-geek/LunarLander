'''
'''

import pygame
from numpy import polynomial as P

tycho = [ -4, -0.1, 11.8, -0.6, -6.1, -0.2, 3.9, 0.8, 0.3 ]


class Mountains(pygame.sprite.Sprite):
    bgcolor = (0, 0, 0)
    clear = (0, 1, 0)
    fgcolor = (80, 80, 80)
    
    def __init__(self, rect):
        super().__init__()
        self.image = pygame.Surface(rect.size, depth=32)
        self.image.set_colorkey(self.clear)
        self.rect = self.image.get_rect(topleft=rect.topleft)
        self.render()
            
    def render(self):
        rect = self.image.get_rect()
        self.image.fill(self.bgcolor)
        pygame.draw.line(self.image, self.fgcolor, rect.topleft, rect.topright, 3)
        
    def update(self, *args):
        pass

class Tycho(pygame.sprite.Sprite):
    bgcolor = (80,80,80, 128)
    clear = (0,1,0)
    fgcolor = (80,80,80)
    
    def __init__(self, rect, n=11):
        super().__init__()
        self.image = pygame.Surface(rect.size, depth=32)
        self.rect = self.image.get_rect(topleft=rect.topleft)
        self.image.set_colorkey(self.clear)

        p = P.Chebyshev(tycho).linspace(n)

        # scale x terms to rect width
        w2 = self.rect.w / 2
        X = (p[0] * w2) + w2

        # scale y terms to rect height
        
        Y = abs(p[1]-p[1][0])
        Y *= (self.rect.h-10) / Y.max()

        # self.points = [self.rect.rect.topleft
        
        pts = [(int(x),int(y)) for x,y in zip(X,Y)]
        
        self.pads = [LandingPad(p,30) for p in pts[1:-1]]

        self.points = [pts[0]]
        
        for p in self.pads:
            self.points.append(p.rect.bottomleft)
            self.points.append(p.rect.bottomright)
            
        self.points.extend([pts[-1],
                            self.rect.bottomright,
                            self.rect.bottomleft])


        # relocate the pad to world coordinates
        for pad in self.pads:
            x,y = pad.rect.center
            a,b = self.rect.topleft
            pad.rect.center = a+x,b+y
        self.render()

        

    def render(self,debug=False):
        self.image.fill(self.clear)
        pygame.gfxdraw.filled_polygon(self.image, self.points, self.fgcolor)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        pass
    

class LandingPad(pygame.sprite.Sprite):
    clear = (0, 1, 0)
    fgcolor = (0, 255, 0)
    
    def __init__(self, xy, width, height=2):
        super().__init__()
        self.image = pygame.Surface((width, height), depth=32)
        self.rect = self.image.get_rect(center = xy)
        self.render()

    def render(self, debug=False):
        self.image.fill(self.clear)
        rect = self.image.get_rect()
        if debug:
            pygame.draw.rect(self.image, (80,80,80), rect, 1)
        pygame.draw.line(self.image, self.fgcolor, rect.bottomleft, rect.bottomright, 3)

