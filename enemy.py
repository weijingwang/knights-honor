import pygame

# dog bark sound effect : https://freesound.org/people/deleted_user_3424813/sounds/260776/

class Enemy(pygame.sprite.Sprite):
    """player"""
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.bark = pygame.mixer.Sound("assets/se/dog_bark_clip.ogg")
        self.bark.set_volume(0.3)
        self.bark_channel = pygame.mixer.Channel(0)
        self.x = x
        self.y = 446
        self.K_LEFT, self.K_RIGHT, self.K_A, self.K_D, self.K_CLICK, self.K_SPACE = False, False, False, False, False, False
        self.image = pygame.image.load("assets/images/KH_BG_1-8.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.attack = False
        
    def draw(self, screen):
        screen.blit(self.image, (self.x,0))


    def follow_player(self, player):
        my_pos = pygame.math.Vector2(self.rect.x, self.rect.y)
        target_pos = pygame.math.Vector2(player.rect.center)
        
        # Calculate direction vector (target - enemy)
        direction = target_pos - my_pos
        
        # Normalize direction to get unit vector (length 1)
        if direction.length() > 0:
            direction = direction.normalize()

        # Move enemy in the direction of the target
        my_pos += direction * 1

        # Update enemy's position
        self.rect.x, self.rect.y = my_pos.x, my_pos.y


    def update(self, player_group):
        self.x = self.rect.x
        self.y = self.rect.y

        for player in player_group:
           self.follow_player(player)

        # self.rect.x+=1
        # print(self.rect.x)
        
        # collided_player = pygame.sprite.spritecollideany(self, player_group)
        # if collided_player:
        #     self.bark.play()
            
        #     self.kill()
        #     print(self.rect)
        #     # print("collided player")
        #     if not self.bark_channel.get_busy():
        #         self.bark_channel.play(self.bark)

        if self.K_LEFT: self.x -= 5
        if self.K_RIGHT: self.x += 5