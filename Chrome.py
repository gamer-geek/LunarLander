'''
'''

import pygame 

FontName = "PressStart2P.ttf"

class Chrome(pygame.sprite.Sprite):
    clear = (0, 1, 0)
    fgcolor = (255, 255, 255)

    def __init__(self, rect, maxGuys, guySprite, score=0):
        super().__init__()
        self.image = pygame.Surface(rect.size,depth=32)
        self.rect = self.image.get_rect()
        self.image.set_colorkey(self.clear)
        self.image.fill(self.clear)
        self.maxGuys = maxGuys
        self.guy = guySprite
        self.guy.render()
        self.score = score
        self.message = None
        self.needsRender = True
        self.render()

    @property
    def font(self):
        try:
            return self._font
        except AttributeError:
            pass
        self._font = pygame.font.Font(FontName, 32)
        return self._font

    @property
    def score(self):
        try:
            return self._score
        except AttributeError:
            pass
        self._score = 0
        return self._score

    @score.setter
    def score(self, newScore):
        self._score = int(newScore)
        self.needsRender = True

    @property
    def message(self):
        try:
            return self._message
        except AttributeError:
            pass
        self._message = None
        return self._message

    @message.setter
    def message(self, newMessage):
        self._message = newMessage
        self.needsRender = True

    @property
    def nguys(self):
        try:
            return self._nguys
        except AttributeError:
            pass
        self._nguys = self.maxGuys
        return self._nguys

    @nguys.setter
    def nguys(self, newValue):
        if newValue < self.maxGuys:
            self.message = 'Crash!'
            
        if newValue < 0:
            self.message = 'Game Over!'
            
        if newValue >= self.maxGuys:
            self.message = 'Ready!'
            
        self._nguys = int(newValue)
        self.needsRender = True

    @property
    def gameOver(self):
        return self.nguys < 0

    @property
    def scoreLabel(self):
        image = self.font.render('{:8d}'.format(self.score),
                                 True,
                                 self.fgcolor,
                                 self.clear)
        self.needsRender = True
        return image


    def reset(self, nguys=3, score=0):
        '''
        '''
        self.nguys = self.maxGuys
        self.score = 0

    def update(self, dt):

        self.render()

    def draw_guys(self, debug=False):
        '''
        '''
        img = self.guy.image
        r = self.guy.rect
        x,y = self.guy.w *3, self.guy.h*3
        for i in range(0, self.nguys):
            r.center = x + (x*i), y
            self.image.blit(img, r)

    def draw_score(self, debug=False):
        '''
        '''
        xy  = self.rect.midtop[0], self.guy.h * 3
        rect = self.scoreLabel.get_rect(center=xy)
        self.image.blit(self.scoreLabel, rect)

    def draw_message(self, debug=False):
        '''
        '''
        if self.message:
            img = self.font.render(self.message, True, self.fgcolor, self.clear)
            rect = img.get_rect(center=self.rect.center)
            self.image.blit(img, rect)

    def draw_labels(self, debug=False):

        self.draw_score(debug)
        
        self.draw_message(debug=debug)

        self.message = None
        
    def render(self, debug=True):

        if self.needsRender:
            
            self.image.fill(self.clear)
        
            # draw guys
            self.draw_guys(debug=debug)

            # draw labels
            self.draw_labels(debug=debug)
            
            self.needsRender = False

        
