import pygame

class Title():
    def __init__(self, image_path):
        self.image= pygame.image.load(image_path).convert_alpha()
        self.done = False
    def run(self, screen):
        screen.blit(self.image, (0,0))
    def check_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.done = True
            

