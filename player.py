import pygame
FPS = 60

"oof sound effect from https://freesound.org/people/dersuperanton/sounds/437651/"
"slash sound effect from https://freesound.org/people/JohnBuhr/sounds/326854/"

class PlayerClass(pygame.sprite.Sprite):
    """player"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.attacking = False
        self.attack_timer = 1 * FPS
        self.attack_timer_store = self.attack_timer

        self.oof = pygame.mixer.Sound("assets/se/oof-clip.ogg")
        self.slash = pygame.mixer.Sound("assets/se/slash-clip.ogg")
        self.HP = 10
        self.left_border, self.right_border = 250, 1150
        self.direction = "right"
        self.K_LEFT, self.K_RIGHT, self.K_A, self.K_D, self.K_CLICK, self.K_SPACE = False, False, False, False, False, False
        self.image_right = pygame.image.load("assets/images/KH_BG_1-4.png").convert_alpha()
        self.image_righta = pygame.image.load("assets/images/KH_BG_1-4a.png").convert_alpha()

        self.image_left= pygame.transform.flip(self.image_right, True, False)
        self.image_lefta= pygame.transform.flip(self.image_righta, True, False)

        self.image = self.image_right

        self.x = 206
        self.y = 256
        self.rect = self.image.get_rect()
        self.rect.width -= 0 # try perfect collison using masks later
        self.rect.topleft = (self.x, self.y)
        self.ground_y = 224

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

        # collided_enemy = pygame.sprite.spritecollideany(self, enemy_group)
        # if collided_enemy:
        #     pass
        #     # print("collided_enemy")
        if self.attacking:
            print(self.attacking)

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

        # if self.rect.x > 1150 - self.rect.w:
        #     self.rect.x = 1150 - self.rect.w
        # elif self.rect.x < 250:
        #     self.rect.x = 250

        



