import pygame

# dog bark sound effect : https://freesound.org/people/deleted_user_3424813/sounds/260776/

class Enemy(pygame.sprite.Sprite):
    """player"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.bark = pygame.mixer.Sound("assets/se/dog_bark_clip.ogg")
        self.bark_channel = pygame.mixer.Channel(0)
        self.x = 752
        self.y = 446
        self.K_LEFT, self.K_RIGHT, self.K_A, self.K_D, self.K_CLICK, self.K_SPACE = False, False, False, False, False, False
        self.image = pygame.image.load("assets/images/KH_BG_1-8.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.attack = False
        
    def draw(self, screen):
        screen.blit(self.image, (self.x,0))
    def update(self, player_group):
        collided_player = pygame.sprite.spritecollideany(self, player_group)
        if collided_player:
            print("collided player")
            if not self.bark_channel.get_busy():
                self.bark.play()
        if self.K_LEFT: self.x -= 5
        if self.K_RIGHT: self.x += 5