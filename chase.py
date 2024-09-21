import pygame


class ChaseGame:
    def __init__(self):
        self.bg_img = pygame.image.load("assets/images/intro/1/bg.png").convert_alpha()
        self.player_img = pygame.image.load("assets/images/intro/1/char.png").convert_alpha()
        self.dwarf_imgs = [pygame.image.load("assets/images/intro/1/dwarf/1.png").convert_alpha(),
                    pygame.image.load("assets/images/intro/1/dwarf/2.png").convert_alpha(),
                    pygame.image.load("assets/images/intro/1/dwarf/3.png").convert_alpha(),
                    pygame.image.load("assets/images/intro/1/dwarf/4.png").convert_alpha(),
                    pygame.image.load("assets/images/intro/1/dwarf/4.png").convert_alpha(),
                    pygame.image.load("assets/images/intro/1/dwarf/4.png").convert_alpha(),
                    pygame.image.load("assets/images/intro/1/dwarf/4.png").convert_alpha(),
                    pygame.image.load("assets/images/intro/1/dwarf/4.png").convert_alpha(),
                    pygame.image.load("assets/images/intro/1/dwarf/4.png").convert_alpha(),
                    pygame.image.load("assets/images/intro/1/dwarf/4.png").convert_alpha(),
                    pygame.image.load("assets/images/intro/1/dwarf/4.png").convert_alpha(),
                    pygame.image.load("assets/images/intro/1/dwarf/4.png").convert_alpha(),
                    pygame.image.load("assets/images/intro/1/dwarf/4.png").convert_alpha(),
                    pygame.image.load("assets/images/intro/1/dwarf/4.png").convert_alpha(),
                    pygame.image.load("assets/images/intro/1/dwarf/5.png").convert_alpha(),
                    pygame.image.load("assets/images/intro/1/dwarf/6.png").convert_alpha(),
                    pygame.image.load("assets/images/intro/1/dwarf/7.png").convert_alpha(),
                    pygame.image.load("assets/images/intro/1/dwarf/8.png").convert_alpha()]
        self.dwarf_index = 0
        self.dwarf_img = self.dwarf_imgs[self.dwarf_index]
        self.done = False
        self.player_x = -500
        self.player_y = 0
        self.player_speed = 10

        self.bg_x = 0
        self.bg_y = 0

        self.bg2_x = 1280
        self.bg2_y = 0

        self.bg_speed = 10

        self.y_move_counter = 15
        self.y_move_counter_store = self.y_move_counter

        self.y_move = 1

        self.stop_move = False

        self.dwarf_animate_counter = 5
        self.dwarf_animate_counter_store = self.dwarf_animate_counter



    def check_events(self):
        self.K_LEFT = pygame.key.get_pressed()[pygame.K_LEFT]
        self.K_a = pygame.key.get_pressed()[pygame.K_a]
        self.K_RIGHT = pygame.key.get_pressed()[pygame.K_RIGHT]
        self.K_d = pygame.key.get_pressed()[pygame.K_d]

    def run(self, screen):
        if not self.stop_move:
            self.check_events()

            self.y_move_counter -= 1
            if self.y_move_counter <= 0:
                self.y_move_counter = self.y_move_counter_store
                self.y_move = self.y_move * -1

            self.player_y += self.y_move * 2
            
            if self.K_LEFT or self.K_a: self.player_x -= self.player_speed
            if self.K_RIGHT or self.K_d: self.player_x += self.player_speed

            self.bg2_x -= self.bg_speed
            self.bg_x -= self.bg_speed
            if self.bg_x <= -1280:
                self.bg_x = 0

            if self.bg2_x <=0:
                self.bg2_x = 1280
            self.dwarf_y = self.player_y -100
        else:
            self.dwarf_animate_counter-=1
            if self.dwarf_animate_counter <=0:
                self.dwarf_animate_counter = self.dwarf_animate_counter_store
                if self.dwarf_index < len(self.dwarf_imgs):
                    self.dwarf_img = self.dwarf_imgs[self.dwarf_index]
                    self.dwarf_index +=1
                else:
                    self.dwarf_y = 0
                    self.player_x = 0

        if self.player_x >= 0:
            self.stop_move = True
        

        screen.blit(self.bg_img, (self.bg_x,self.bg_y))
        screen.blit(self.bg_img, (self.bg2_x,self.bg2_y))
        screen.blit(self.player_img, (self.player_x,self.player_y))
        screen.blit(self.dwarf_img, (0,self.dwarf_y))


