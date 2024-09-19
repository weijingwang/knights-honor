import pygame


class Thing(pygame.sprite.Sprite):
    """interactable object"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
    
        self.image_righta = pygame.image.load("assets/images/KH_BG_1-4a.png").convert_alpha()

        self.rect = self.image.get_rect()
        
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
    def update(self):
        pass