#!/usr/bin/env python3.4

import sys
import time
import pygame
from pygame.locals import *

from Geometry import Point
from random import randint

from Game import WASDGame
from Lander import Lander
from Landscape import Tycho, LandingPad
from Sky import Star


# G(e) = 9.80 m/s^2
# G(l) = 1.62 m/s^2

G_Moon = 1.63

class LunarLanderGame(WASDGame):

    # draw layer z-order
    RESERVE     = 5
    FOREGROUND  = 4
    LANDINGPADS = 3
    TERRAIN     = 2
    SKYBOX      = 1
    
    BLACK=(0,0,0)
    
    def __init__(self):
        super().__init__(1024, 1024)
        
        pygame.display.set_caption('Lunar Lander Demo')
        self.gravity = G_Moon
        self.scale = 1 # pixels per meter
        self.paused = False
        self.gameOver = False
        
        self.add_event(QUIT,       self.quit)
        self.add_control(K_q,      self.handle_q)
        self.add_control(K_e,      self.handle_e)
        self.add_control(K_SPACE,  self.handle_space)
        self.add_control(K_ESCAPE, self.handle_escape)
        self.add_control(K_LSHIFT, self.handle_lshift)
        self.add_control(K_LCTRL,  self.handle_lcontrol)
        self.add_control(K_x,      self.handle_x)
        self.add_control(K_z,      self.handle_z)

        self.sprites = pygame.sprite.LayeredUpdates()

        # XXX order sensitive
        self.sprites.add(self.stars)
        self.sprites.add(self.crater)
        for pad in self.crater.pads:
            pad.layer = self.LANDINGPADS
        self.sprites.add(self.crater.pads)
        self.sprites.add(self.lander)
        self.sprites.add(self.guys)
    
    @property
    def horizon(self):
        try:
            return self._horizon
        except AttributeError:
            pass
        self._horizon = (self.bounds.h / 4) * 3
        return self._horizon

    @property
    def skybox(self):
        try:
            return self._skybox
        except AttributeError:
            pass
        
        self._skybox = pygame.rect.Rect((0,0), self.bounds.size)
        return self._skybox

    @property
    def terrainbox(self):
        try:
            return self._terrainbox
        except AttributeError:
            pass
        h = self.bounds.h - self.horizon
        self._terrainbox = pygame.rect.Rect((0,self.horizon), (self.bounds.w, h))
        return self._terrainbox
    
    @property
    def crater(self):
        try:
            return self._crater
        except AttributeError:
            pass
        self._crater = Tycho(self.terrainbox, 11)
        self._crater.layer = self.TERRAIN
        return self._crater

    @property
    def start(self):
        try:
            return self._start
        except AttributeError:
            pass
        x,y = self.bounds.center
        y -= y/4
        self._start = x,y
        return self._start

    @property
    def lander(self):
        try:
            return self._lander
        except AttributeError:
            pass
        self._lander = Lander(self.start, self.gravity)
        self._lander.layer = self.FOREGROUND
        return self._lander

    @property
    def guys(self):
        try:
            return self._guys
        except AttributeError:
            pass
        self._guys = []
        for i in range(0, 3):
            l = Lander((0,0), self.gravity)
            x,y = l.w * 3, l.h * 3
            l.position.xy = x + (x*i), y
            l.heading = 90
            l.layer = self.RESERVE
            l.noUpdate = True
            self._guys.append(l)

        return self._guys
        
    @property
    def stars(self):
        try:
            return self._stars
        except AttributeError:
            pass

        r = self.skybox
        p = lambda r:(randint(r.x,r.w), randint(r.y,r.h))
        self._stars = [Star(p(r)) for _ in range(0,30)]
        for star in self._stars:
            star.layer = self.SKYBOX
        return self._stars

    def keyUp(self, keycode):
        pass

    def keyDown(self, keycode):

        if keycode.dict['key'] == K_SPACE:
            self.paused = not self.paused
            return
        pass

    def handle_q(self):
        self.lander.rotate(5)

    def handle_e(self):
        self.lander.rotate(-5)
        pass

    def handle_escape(self):
        self.quit()

    def handle_space(self):
        pass

    def handle_lshift(self):
        self.lander.throttle += 5

    def handle_lcontrol(self):
        self.lander.throttle -= 5        

    def handle_z(self):
        self.lander.throttle = 100
        
    def handle_x(self):
        self.lander.throttle = 0
        
    def check_bounds(self):
        '''
        '''

        if self.lander.crashed:
            return
        
        if self.lander.rect.centery > self.bounds.h:
            self.lander.crashed = True

        if self.lander.rect.centery < 0:
            self.lander.rect.centery = 0

        if self.lander.position.x < 0:
            self.lander.position.x = self.bounds.w
            
        if self.lander.position.x > self.bounds.w:
            self.lander.position.x = 0

    def check_collisions(self):
        '''
        '''

        if pygame.sprite.collide_mask(self.lander, self.crater):
            self.lander.crashed = True
        
        if not self.lander.crashed:
            self.lander.collidelist(self.crater.pads)
        
    def update(self):
        '''
        '''

        if self.lander.crashed:
            try:
                self.sprites.remove(self.guys.pop())
                self.lander.reset(self.start)
            except IndexError:
                self.gameOver = True

        if self.paused:
            self.deltaTime
            return
        
        self.sprites.update(self.deltaTime)

        self.check_bounds()

        self.check_collisions()

        if self.lander.landed:
            self.lander.velocity.xy = (0,0)


    def draw(self):
        '''
        '''

        self.screen.fill((0,0,0))
        
        return self.sprites.draw(self.screen)

    def quit(self, event=None):
        '''
        '''
        exit()

    def run(self):
        '''
        '''
        while True:
            self.dispatch_events()
            self.dispatch_keypress()
            self.update()
            pygame.display.update(self.draw())


if __name__ == '__main__':
        LunarLanderGame().run()
        

