#!/usr/bin/env python3.4

import sys
import time
import pygame
from pygame.locals import *

from Geometry import Point
from random import randint

from Game import WASDGame
from Lander import Lander
from Effects import SimpleExplosion
from Landscape import Tycho, LandingPad
from Sky import Star
from Chrome import Chrome


# G(e) = 9.80 m/s^2
# G(l) = 1.62 m/s^2

G_Moon = 1.63

FontName = 'PressStart2P.ttf'

class LunarLanderGame(WASDGame):

    # draw layer z-order
    CHROME      = 6
    EXPLOSIONS  = 5
    FOREGROUND  = 4
    LANDINGPADS = 3
    TERRAIN     = 2
    SKYBOX      = 1
    
    BLACK=(0,0,0)
    
    def __init__(self):
        super().__init__(1024, 1024)
        
        pygame.display.set_caption('Lunar Lander Demo')

        pygame.chrome = self.screen.copy()

        self.gravity = G_Moon
        self.scale = 1 # pixels per meter
        self.paused = False
        self.hesitating = False
        self.gameOver = False
        self.frames = 0
        
        self.add_event(QUIT,       self.quit)
        self.add_control(K_q,      self.handle_q)
        self.add_control(K_e,      self.handle_e)
        self.add_control(K_SPACE,  self.handle_space)
        self.add_control(K_ESCAPE, self.handle_escape)
        self.add_control(K_LSHIFT, self.handle_lshift)
        self.add_control(K_LCTRL,  self.handle_lcontrol)
        self.add_control(K_x,      self.handle_x)
        self.add_control(K_z,      self.handle_z)

        self.game_scene = pygame.sprite.LayeredUpdates()

        # XXX order sensitive
        self.game_scene.add(self.stars)
        self.game_scene.add(self.crater)
        for pad in self.crater.pads:
            pad.layer = self.LANDINGPADS
        self.game_scene.add(self.crater.pads)
        self.game_scene.add(self.lander)
        self.game_scene.add(self.chrome)
    
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

    @property
    def chrome(self):
        try:
            return self._chrome
        except AttributeError:
            pass

        self._chrome = Chrome(self.bounds, 2, Lander((0,0), 0))
        self._chrome.layer = self.CHROME
        
        return self._chrome


    def keyUp(self, keycode):
        pass

    def keyDown(self, keycode):

        if keycode.dict['key'] == K_SPACE:

            if self.chrome.gameOver:
                self.chrome.reset()
                return
            
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

        if self.lander.crashed or self.lander.landed:
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

        # collide with landing pads
        if not self.lander.crashed:
            self.lander.collidelist(self.crater.pads)

        if self.lander.landed or self.lander.crashed:
            return

        # collide with terrain
        
        if pygame.sprite.collide_mask(self.lander, self.crater):
            self.lander.crashed = True

        
    def update(self):
        '''
        '''

        dt = self.deltaTime
        
        if self.paused:
            return

        if self.chrome.gameOver:
            return

        if self.hesitating:
            self.frames += 1
            self.hesitating = (self.frames < 50)
            self.game_scene.update(dt)
            if not self.hesitating:
                self.chrome.message = None
                self.chrome.render()
                self.lander.reset(self.start)
                self.game_scene.add(self.lander)
            return

        self.game_scene.update(dt)

        self.check_bounds()

        self.check_collisions()

        if self.lander.landed:
            return
        
        if self.lander.crashed:
            if self.lander.alive():
                e = SimpleExplosion(self.lander.position.xy,
                                    max(self.lander.rect.w,self.lander.rect.h),
                                    layer = self.EXPLOSIONS,
                                    generation=5)
                self.game_scene.add(e)
                self.lander.kill()
                self.chrome.nguys -= 1
                self.chrome.render()
                self.hesitating = True
                self.frames = 0


    def draw(self):
        '''
        '''

        self.screen.fill((0,0,0))
        
        return self.game_scene.draw(self.screen)

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
        

