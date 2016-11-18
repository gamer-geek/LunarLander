'''
'''


import pygame
import math
from Geometry import Point

class StaticVehicle(pygame.sprite.Sprite):
    
    def __init__(self, xy, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height), 32)
        self.rect = self.image.get_rect(center=xy)
        self.position = Point(xy)

class MovingVehicle(StaticVehicle):
    def __init__(self, xy, width, height, heading = 0, velocity=Point()):
        super().__init__(xy, width, height)
        self.needsRender = True
        self.heading = heading
        self.velocity = velocity

    @property
    def heading(self):
        try:
            return self._heading
        except AttributeError:
            pass
        self._heading = 90.
        return self._heading

    @heading.setter
    def heading(self, newValue):
        newValue %= 360
        if newValue != self.heading:
            self._heading = float(newValue)
            self.needsRender = True        
        

class AcceleratingVehicle(MovingVehicle):

    def __init__(self, xy, width, height,  maxAcceleration, heading=90, initialVelocity = Point()):
        super().__init__(xy, width, height, heading, initialVelocity)
        self.maxAcceleration = maxAcceleration # scalar

    def __str__(self):
        fmt = []
        fmt.append('XY {v.position.x:6.1f},{v.position.y:6.1f}')
        fmt.append(' V {v.velocity.x:6.1f},{v.velocity.y:6.1f}')
        fmt.append(' A {v.acceleration.x:6.1f},{v.acceleration.y:6.1f}')

        return ' '.join(fmt).format(v=self)
        
    @property
    def throttle(self):
        try:
            return self._throttle
        except AttributeError:
            pass
        self._throttle = 0
        return self.throttle

    @throttle.setter
    def throttle(self, newValue):
        if newValue < 0:
            newValue = 0
        if newValue > 100:
            newValue = 100
        self._throttle = newValue
        self.needsRender = True

    @property
    def acceleration(self):
        if self.throttle > 0:
            f = self.maxAcceleration * (self.throttle/100)
            r = math.radians(360 - self.heading)
            return Point(math.cos(r) * f, math.sin(r) * f)
        try:
            return self._zeroAcceleration
        except AttributeError:
            pass
        self._zeroAcceleration = Point()
        return self._zeroAcceleration


    def move(self, dt, gravity=Point(), drag=Point()):
        '''
        '''
        prev = Point(self.position)
        A = self.acceleration + gravity + drag
        self.velocity += A * dt
        self.position += self.velocity
        return prev
        
