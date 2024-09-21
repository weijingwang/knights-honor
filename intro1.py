import pygame
import math


class Intro1:
    def __init__(self, screen, num, speed=6, amplitude=100, frequency=0.05):
        self.screen = screen
        self.num = num
        if self.num == 1:
            self.x = -500  # Starting x position
            self.bg= pygame.image.load("assets/images/intro/1/bg.png").convert_alpha()
            self.image= pygame.image.load("assets/images/intro/1/char.png").convert_alpha()
        elif self.num == 10:
            speed = 6
            amplitude = 10
            frequency = 10
            self.x = 0
            self.bg= pygame.image.load("assets/images/intro/10/bg.png").convert_alpha()
            self.image= pygame.image.load("assets/images/intro/10/char.png").convert_alpha()
        self.speed = speed
        self.amplitude = amplitude
        self.frequency = frequency
        
        self.t = 0  # Time parameter for y-axis movement
        self.screen_width, self.screen_height = self.screen.get_size()
        self.done = False
        self.y = 0


    def check_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.done = True

    def calculate_y(self):
        """Calculate the y position based on abs(sin(t))."""
        return int(0 - self.amplitude * abs(math.sin(self.frequency * self.t)))
    
    def update(self, screen):
        """Update the position of the rectangle."""
        # Calculate the y position
        self.y = self.calculate_y()
        
        # Move the rectangle along the x-axis only when y is changing (cos(t) not near 0)
        if abs(math.cos(self.frequency * self.t)) > 0.001:
            self.x += self.speed
        
        # Check if the rectangle has reached the right side of the screen
        if self.x > self.screen_width:
            self.done = True  # Return False to signal end of movement
        
        # Draw the rectangle
        screen.blit(self.bg, (0,0))
        screen.blit(self.image, (self.x,self.y))        
        # Increment time
        self.t += 1

