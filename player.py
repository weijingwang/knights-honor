import pygame
FPS = 60
SCREEN_LEFT_BOUNDx = 0
SCREEN_RIGHT_BOUNDx = 1280

GRAVITY = 1
SCREEN_HEIGHT = 720
JUMP_STRENGTH = -25
CRIT_MULT = 2
NO_CRIT_MULT = 1
TOTAL_LIVES = 10
"oof sound effect from https://freesound.org/people/dersuperanton/sounds/437651/"
"slash sound effect from https://freesound.org/people/JohnBuhr/sounds/326854/"

class PlayerClass(pygame.sprite.Sprite):
    """player"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.attacking = False
        self.attack_timer = 0.2 * FPS
        self.attack_timer_store = self.attack_timer

        self.attack_cooldown_timer = 1 * FPS
        self.attack_cooldown_timer_store = self.attack_cooldown_timer
        self.cooldown_timer_start = False

        self.oof = pygame.mixer.Sound("assets/se/oof-clip.ogg")
        self.slash = pygame.mixer.Sound("assets/se/slash-clip.ogg")
        self.HP = TOTAL_LIVES
        self.direction = "right"
        self.K_LEFT, self.K_RIGHT, self.K_A, self.K_D, self.K_CLICK, self.K_SPACE = False, False, False, False, False, False
        self.image_right = pygame.image.load("assets/images/KH_BG_1-4.png").convert_alpha()
        self.image_righta = pygame.image.load("assets/images/KH_BG_1-4a.png").convert_alpha()

        self.image_left= pygame.transform.flip(self.image_right, True, False)
        self.image_lefta= pygame.transform.flip(self.image_righta, True, False)

        self.image = self.image_right

        self.x = 1280/2
        self.y = 256
        self.rect = self.image.get_rect()
        self.rect.width -= 0 # try perfect collison using masks later
        self.rect.topleft = (self.x, self.y)
        
        self.is_jumping = False

        self.rect.y = SCREEN_HEIGHT - self.rect.height - 100
        self.ground_y = self.rect.y + self.rect.height
        self.critical_attack = False
        self.crit_multiplier = NO_CRIT_MULT

    def jump(self):
        if self.is_jumping:
            self.critical_attack = True
            self.crit_multiplier = CRIT_MULT
            self.rect.y += self.jump_velocity
            self.jump_velocity += GRAVITY
            if self.rect.y >= SCREEN_HEIGHT - self.rect.height - 100:
                self.rect.y = SCREEN_HEIGHT - self.rect.height - 100
                # print("asdf")
                self.is_jumping = False
                self.critical_attack = False
                self.crit_multiplier = 1
        if not self.is_jumping:
            # self.is_jumping = True
            self.jump_velocity = JUMP_STRENGTH


    def wait_time_done(self):
        self.attack_timer -= 1
        if self.attack_timer <= 0:
            self.attack_timer = self.attack_timer_store
            return True
        else:
            return False

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
    def update(self, enemy_group):
        if self.cooldown_timer_start:
            if self.attack_cooldown_timer > 0:
                self.attack_cooldown_timer -= 1
            else:
                self.attack_cooldown_timer = self.attack_cooldown_timer_store
                self.cooldown_timer_start = False

        self.jump()
        # collided_enemy = pygame.sprite.spritecollideany(self, enemy_group)
        # if collided_enemy:
        #     pass
        #     # print("collided_enemy")
        if self.attacking:
            # self.cooldown_timer_start = True
            if self.attack_cooldown_timer == self.attack_cooldown_timer_store:
                if self.wait_time_done():
                    self.attacking = False
                    if self.direction == "right":
                        self.image = self.image_right
                    elif self.direction == "left":
                        self.image = self.image_left
                else:
                    if self.direction == "right":
                        self.image = self.image_righta
                    elif self.direction == "left":
                        self.image = self.image_lefta
            else:
                self.attacking = False



        if (self.K_LEFT or self.K_a) and self.rect.left >= SCREEN_LEFT_BOUNDx:
            self.rect.x -= 5
            if self.direction == "right":
                self.direction = "left"
                self.image = self.image_left

        if (self.K_RIGHT or self.K_d) and self.rect.right <= SCREEN_RIGHT_BOUNDx:
            self.rect.x += 5
            if self.direction == "left":
                self.direction = "right"
                self.image = self.image_right

        # if self.rect.x > 1150 - self.rect.w:
        #     self.rect.x = 1150 - self.rect.w
        # elif self.rect.x < 250:
        #     self.rect.x = 250

        



