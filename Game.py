'''
'''

import pygame
from pygame.locals import *

class BaseGame(object):
    def __init__(self, width, height, framerate=60):
        pygame.init()
        self.bounds = pygame.rect.Rect((0, 0), (width, height))
        self.screen = pygame.display.set_mode(self.bounds.size, 0, 32)
        self.framerate = framerate
        self.events = {}
        self.controls = {}

    @property
    def clock(self):
        try:
            return self._clock
        except AttributeError:
            pass
        self._clock = pygame.time.Clock()
        return self._clock
        
    @property
    def deltaTime(self):
        return self.clock.tick(self.framerate) / 1000.0

    def add_event(self, event, action):
        name = pygame.event.event_name(event)
        self.events.setdefault(name, action)

    def add_control(self, keycode, action):
        self.controls.setdefault(keycode, action)

    def dispatch_keypress(self):
        presses = pygame.key.get_pressed()
        for key, action in self.controls.items():
            if presses[key]:
                action()
                
    def dispatch_events(self):
        for event in pygame.event.get():
            name = pygame.event.event_name(event.type)
            try:
                self.events[name](event)
            except KeyError:
                pass


class WASDGame(BaseGame):

    def __init__(self, width, height, framerate=60,):
        super().__init__(width, height, framerate)

        self.add_event(KEYUP,   self.keyUp)
        self.add_event(KEYDOWN, self.keyDown)
        self.add_control(K_w,   self.handle_w)
        self.add_control(K_a,   self.handle_a)
        self.add_control(K_s,   self.handle_s)
        self.add_control(K_d,   self.handle_d)

    def keyUp(self, keycode):
        '''
        '''
        pass

    def keyDown(self, keycode):
        '''
        '''
        pass

    def handle_w(self):
        '''
        '''
        pass

    def handle_a(self):
        '''
        '''
        pass

    def handle_s(self):
        '''
        '''
        pass

    def handle_d(self):
        '''
        '''
        pass

    
