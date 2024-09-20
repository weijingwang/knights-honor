import pygame


class Intro2:
    def __init__(self, screen, speed=2):
        self.screen = screen
        self.bg= pygame.image.load("assets/images/intro/3/bg.png").convert_alpha()
        self.image= pygame.image.load("assets/images/intro/3/char.png").convert_alpha()
        self.speed = speed

        self.x = 0  # Starting x position
        self.done = False
        self.y = 0
        self.endx = -700
        self.endy=-400
    
    def check_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.done = True

    def update(self, screen):
        screen.blit(self.bg, (self.x,self.y))
        screen.blit(self.image, (30,30))     
        if self.x>= self.endx:self.x -= self.speed
        if self.y >=self.endy: self.y-=self.speed

        if self.x <=self.endx and self.y <=self.endy:
            self.done = True


