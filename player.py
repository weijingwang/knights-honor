import pygame

class PlayerClass(pygame.sprite.Sprite):
    """player"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.left_border, self.right_border = 250, 1150
        self.direction = "right"
        self.K_LEFT, self.K_RIGHT, self.K_A, self.K_D, self.K_CLICK, self.K_SPACE = False, False, False, False, False, False
        self.image_right = pygame.image.load("assets/images/KH_BG_1-4.png").convert_alpha()
        self.image_left= pygame.transform.flip(self.image_right, True, False)
        self.image = self.image_right
        self.attack = False
        self.x = 206
        self.y = 256
        self.rect = self.image.get_rect()
        self.rect.width -= 0 # try perfect collison using masks later
        self.rect.topleft = (self.x, self.y)
        self.ground_y = 224
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
    def update(self, enemy_group):
        # collided_enemy = pygame.sprite.spritecollideany(self, enemy_group)
        # if collided_enemy:
        #     pass
        #     # print("collided_enemy")
        if self.K_LEFT:
            self.rect.x -= 5
            if self.direction == "right":
                self.direction = "left"
                self.image = self.image_left
            
        if self.K_RIGHT:
            self.rect.x += 5
            if self.direction == "left":
                self.direction = "right"
                self.image = self.image_right




