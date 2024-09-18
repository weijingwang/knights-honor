import pygame
FOLLOW_SPEED = 1
GRAVITY = 0.2
SCREEN_HEIGHT = 720
JUMP_STRENGTH = -3.4
KNOCKBACK_DIST = 200
FPS = 60
# dog bark sound effect : https://freesound.org/people/deleted_user_3424813/sounds/260776/

class Enemy(pygame.sprite.Sprite):
    """player"""
    def __init__(self, x):
        self.time = 1
        self.timer = self.time * FPS
        self.lives = 3 - 1
        self.knockbacked = False
        pygame.sprite.Sprite.__init__(self)
        self.bark = pygame.mixer.Sound("assets/se/dog_bark_clip.ogg")
        self.oof = pygame.mixer.Sound("assets/se/oof-clip.ogg")

        self.bark.set_volume(0.3)
        self.bark_channel = pygame.mixer.Channel(0)
        self.x = x
        self.y = 446
        self.K_LEFT, self.K_RIGHT, self.K_A, self.K_D, self.K_CLICK, self.K_SPACE = False, False, False, False, False, False
        self.image_R = pygame.image.load("assets/images/KH_BG_1-8.png").convert_alpha()
        self.image_L = pygame.transform.flip(self.image_R, True, False)
        self.image = self.image_R
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.attack = False
        self.can_attack = False

        self.jump_velocity = JUMP_STRENGTH
        self.is_jumping = False
        self.facing_right = True

        self.time_seg1 = 1 * FPS
        self.time_seg1_store = self.time_seg1

    def wait_time_done(self):
        self.time_seg1 -= 1
        if self.time_seg1 <= 0:
            self.time_seg1 = self.time_seg1_store
            return True
        else:
            return False


    def attack_movement(self):
        if self.is_jumping:
            self.rect.y += self.jump_velocity
            self.jump_velocity += GRAVITY
            if self.rect.y >= SCREEN_HEIGHT - self.rect.height - 100:
                self.rect.y = SCREEN_HEIGHT - self.rect.height - 100
                # print("asdf")
                self.is_jumping = False
        if not self.is_jumping:
            self.is_jumping = True
            self.jump_velocity = JUMP_STRENGTH

        print(self.time_seg1)

        

    def draw(self, screen):
        screen.blit(self.image, (self.x,0))

    def knockback(self):
        if self.facing_right:
            self.rect.x += KNOCKBACK_DIST
        else:
            self.rect.x -= KNOCKBACK_DIST
        self.lives -= 1
        self.knockbacked = False

            

    def jump(self):
        if self.is_jumping:
            self.rect.y += self.jump_velocity
            self.jump_velocity += GRAVITY
            if self.rect.y >= SCREEN_HEIGHT - self.rect.height - 100:
                self.rect.y = SCREEN_HEIGHT - self.rect.height - 100
                # print("asdf")
                self.is_jumping = False
        if not self.is_jumping:
            self.is_jumping = True
            self.jump_velocity = JUMP_STRENGTH


    def follow_player(self, player):
        my_pos = pygame.math.Vector2(self.rect.x, self.rect.y)
        target_pos = pygame.math.Vector2(player.rect.center)
        
        # Calculate direction vector (target - enemy)
        direction = target_pos - my_pos
        # what way is it moving?
        if direction.x > 0:
            self.facing_right = False
        else:
            self.facing_right = True

        # print(direction)
        # Normalize direction to get unit vector (length 1)
        if direction.length() > 0:
            direction = direction.normalize()

        # Move enemy in the direction of the target
        my_pos += direction * FOLLOW_SPEED

        # Update enemy's position
        self.rect.x, self.rect.y = my_pos.x, my_pos.y


    def update(self, player_group):

        if not self.knockbacked:
            if self.facing_right:
                self.image = self.image_R
            else:
                self.image = self.image_L
            self.jump()
            self.x = self.rect.x
            self.y = self.rect.y

            for player in player_group:
                self.follow_player(player)
        else:
            self.knockback()

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