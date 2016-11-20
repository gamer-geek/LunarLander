'''
'''

import pygame
import pygame.gfxdraw
import math
from random import randint
from Geometry import Point
from Vehicle import AcceleratingVehicle
from Effects import SimpleExplosion

class FuelTank(object):
    '''
    Fuel tanks are delta V reservoirs.
    Put fuel in, get deltaV out.
    '''
    def __init__(self, maxFuel, startFuel=-1, unitsPerSecond=1, deltaVPerUnit=1):
        self.maxFuel = maxFuel
        if startFuel < 0:
            startFuel = maxFuel
        self.fuel = startFuel
        self.ups = unitsPerSecond
        self.dvpu = deltaVPerUnit

    def deltaV(self, deltaTime, consume=True):
        if self.fuel <= 0:
            return 0.0
        units = self.ups * deltaTime
        if self.fuel - units <= 0:
            units = self.fuel
        return units * self.dvpu

        
class Lander(AcceleratingVehicle):

    clear = (0, 1, 0)
    bgcolor = (0, 0, 0)
    fgcolor = (255, 255, 255)
    
    def __init__(self, xy, gravity, fuel=100, width=11, height=11):
        '''
        '''
        super().__init__(xy, width*8, height*8, 3*gravity)

        self.w = width
        self.h = height
        
        self.gravity = Point(0, gravity)

        self.drawbuf = pygame.Surface(self.rect.size, depth=32)
        self.drawbuf.set_colorkey(self.clear)
        
        self.legs = pygame.rect.Rect((0,0), (2*width, (2*height)+1))
        self.hull = pygame.rect.Rect((0,0), (width, height))
        self.plume = pygame.rect.Rect((0,0), (3*width, height - 2))
        self.hull.center = self.drawbuf.get_rect().center
        self.cabin = self.hull.inflate(width/2, height/2)
        self.service = self.cabin.inflate(-width, 0)
        self.service.center = self.cabin.midleft
        
        self.legs.midright = self.hull.midright
        self.plume.midright = self.hull.midleft
        self.drymass = 10
        
        self.reset(xy, fuel)

    def reset(self, xy, fuel=100):
        self.position.xy = xy
        self.fuel = fuel
        self.velocity.xy = 0,0
        self.throttle = 0
        self.crashed = False
        self.landed = False
        self.needsRender = True
        self.heading = 90
        self.image.fill(self.clear)


    @property
    def mass(self):
        return self.drymass + self.fuel


    @property
    def crashed(self):
        try:
            return self._crashed
        except AttributeError:
            pass
        self._crashed = False
        return self._crashed

    @crashed.setter
    def crashed(self, newValue):
        self.needsRender = True
        self._crashed = newValue

    @property
    def landed(self):
        try:
            return self._landed
        except AttributeError:
            pass
        self._landed = False

    @landed.setter
    def landed(self, newValue):
        if newValue:
            self.velocity.xy = 0,0
            self.throttle = 0
            
        self.needsRender = True
        self._landed = newValue

    @property
    def probe(self):
        x,y = (self.position + (0, self.h * 1.5)).xy
        return int(x),int(y)

    @property
    def goodLanding(self):
        dVx = abs(self.velocity.x) < self.gravity.y
        dVy = self.velocity.y < (2*self.gravity.y)
        H   = abs(self.heading-90) <= 10
        return dVx and dVy and H
        

    def colliderect(self, rect):
        '''
        '''
        #if self.velocity.y > rect.h:
        #     r = pygame.rect.Rect((0, 0), self.velocity.xy)
        #     r.center = self.probe
        #     return rect.colliderect(r)

        return rect.collidepoint(self.probe)

    def collidelist(self, spritelist):
        '''
        '''
        
        for s in spritelist:
            if not self.landed and self.colliderect(s.rect):
                self.landed = self.goodLanding
                self.crashed = not self.goodLanding
                return s
            
        self.landed = False
        self.crashed = False
        
        return None
        
    def rotate(self, degrees):
        self.heading += degrees

    def doExplosion(self):
        e = SimpleExplosion(self.position.xy,
                            max(self.rect.w,self.rect.h),
                            layer=self.layer,generation=0)
        e.add(self.groups())
        self.kill()

    def update(self, dt):

        if self.alive() and self.crashed:
            self.doExplosion()
            return

        prev = self.move(dt, gravity=self.gravity)
        if self.landed:
            self.position.xy = map(int,prev.xy)

        self.render()


    def debug_draw(self,draw=False):
        if draw:
            r = self.drawbuf.get_rect()
            c = (80,80,80)
            pygame.draw.rect(self.drawbuf, c, r, 1)
            pygame.draw.line(self.drawbuf, c, r.midleft, r.midright, 1)
            pygame.draw.line(self.drawbuf, c, r.midtop, r.midbottom, 1)
            pygame.draw.rect(self.drawbuf, c, self.legs, 1)
            pygame.draw.rect(self.drawbuf, c, self.plume, 1)

    def draw_exhaust(self):
        '''
        '''
        
        if self.throttle == 0:
            return
        
        r = self.plume.copy()
        r.w = int(self.plume.w * (self.throttle / 100))

        if r.w < 1:
            return
        
        x,y = self.hull.midleft
        r.midright = x-5, y

        outline = [r.topright, r.midleft, r.bottomright]

        pygame.gfxdraw.filled_polygon(self.drawbuf, outline, (255, 0, 0))

        r.inflate_ip(-4,-4)
        r.normalize()

        p = randint(r.midleft[0], r.center[0]), r.midleft[1]
        
        outline = [r.topright, p, r.bottomright]
        pygame.draw.polygon(self.drawbuf, (0,255,0), outline, 1)

    def draw_lander(self):
        pygame.draw.ellipse(self.drawbuf, self.bgcolor, self.cabin, 0)
        pygame.draw.ellipse(self.drawbuf, self.fgcolor, self.cabin, 1)
                            
        for a,b in [ (self.legs.topleft, self.hull.topleft),
                     (self.legs.bottomleft, self.hull.bottomleft)]:
            pygame.draw.line(self.drawbuf, self.fgcolor, a, b, 1)
            
        self.drawbuf.fill(self.fgcolor, self.service)

        w = self.hull.width / 5
        for x,y in [self.legs.topleft, self.legs.bottomleft]:
            pygame.draw.line(self.drawbuf, self.fgcolor, (x,y-w), (x,y+w), 1)

        return self.rect
        

    def render(self, debug=False):
            
        if self.needsRender:
            self.drawbuf.fill(self.clear)
            self.debug_draw(debug)
            self.draw_lander()
            self.mask = pygame.mask.from_surface(pygame.transform.rotate(self.drawbuf, self.heading))
            self.draw_exhaust()
            self.image = pygame.transform.rotate(self.drawbuf, self.heading)
            self.needsRender = False

        self.rect = self.image.get_rect(center=self.position.xy)
        
