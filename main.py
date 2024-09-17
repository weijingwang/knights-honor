import pygame
from player import PlayerClass
from enemy import Enemy
from camera import Camera

class Game():
    """basic game"""
    def __init__(self):
        
        pygame.mixer.pre_init()
        pygame.init()
        self.bark = pygame.mixer.Sound("assets/se/dog_bark_clip.ogg")
        self.bark.set_volume(0.3)

        self.FPS = 60
        # pygame.display.set_caption("knight's honor (pygame 38)")
        self.key = pygame.key.get_pressed()
        self.clock = pygame.time.Clock()
        self.DISPLAY_W, self.DISPLAY_H = 1280, 720
        self.K_LEFT, self.K_RIGHT, self.K_A, self.K_D, self.K_CLICK, self.K_SPACE = False, False, False, False, False, False

        self.screen = pygame.Surface((self.DISPLAY_W,self.DISPLAY_H))
        self.window = pygame.display.set_mode((self.DISPLAY_W,self.DISPLAY_H))

        self.done = False

        self.font = pygame.font.get_default_font()

        self.bg1 = pygame.image.load("assets/images/KH_BG_1-1.png").convert_alpha()
        self.bg2 = pygame.image.load("assets/images/KH_BG_1-2.png").convert_alpha()
        self.bg3 = pygame.image.load("assets/images/KH_BG_1-3.png").convert_alpha()

        pygame.mixer.music.load("assets/music/colyon-clip.ogg")
        pygame.mixer.music.play(-1,0.0)
        pygame.mixer.music.set_volume(0.5)

        self.player = PlayerClass()
        self.dog = Enemy(752)
        self.dog2 = Enemy(-300)
        self.all_sprites = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()

        self.player_group.add(self.player)
        self.enemy_group.add(self.dog)
        self.enemy_group.add(self.dog2)

        # self.all_sprites.add(self.player)
        # self.all_sprites.add(self.dog)
        # self.all_sprites.add(self.dog2)

        self.camera = Camera(self.player)

        self.bgx=0
        self.bgy=0



        

    def check_events(self):
        self.player.K_LEFT = pygame.key.get_pressed()[pygame.K_LEFT]
        self.player.K_RIGHT = pygame.key.get_pressed()[pygame.K_RIGHT]
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                       self.done = True
                # if event.type == pygame.KEYDOWN:
                #     # self.K_LEFT, self.K_RIGHT, self.K_A, self.K_D, self.K_CLICK, self.K_SPACE
                #     if event.key == pygame.K_LEFT: self.K_LEFT = True
                #     if event.key == pygame.K_BACKSPACE: self.BACK_KEY = True
                #     if event.key == pygame.K_DOWN: self.DOWN_KEY = True
                #     if event.key == pygame.K_UP: self.UP_KEY = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE: self.player.attack = True
                #     if event.key == pygame.K_BACKSPACE: self.BACK_KEY = True
                #     if event.key == pygame.K_DOWN: self.DOWN_KEY = True
                #     if event.key == pygame.K_UP: self.UP_KEY = True
    def game_loop(self):
        while not self.done:
            self.screen.fill((0,0,0))
            self.check_events()

            self.bgx -= self.camera.offset.x
            self.bgy -= self.camera.offset.y
            self.screen.blit(self.bg1, (self.bgx, self.bgy))
            self.screen.blit(self.bg2, (self.bgx, self.bgy))
            self.screen.blit(self.bg3, (self.bgx, self.bgy))
            
            self.player.rect.x = self.player.rect.x - self.camera.offset.x
            self.player.rect.y = self.player.rect.y - self.camera.offset.y

            self.player.update(self.enemy_group)

            for enemy in self.enemy_group:
                enemy.rect.x  -= self.camera.offset.x
                enemy.rect.y -= self.camera.offset.y

            self.enemy_group.update(self.player_group) #use enemy group instead of updating individul enemy so that when enemy is killed, it is removed from group and not revived with the update function
            


    #     canvas.blit(house, (0 - camera.offset.x, 0 - camera.offset.y))
    # canvas.blit(cat.current_image,(cat.rect.x - camera.offset.x, cat.rect.y - camera.offset.y))

            # See if shots hit the aliens.
            for enemy in pygame.sprite.groupcollide(self.enemy_group, self.player_group, 0, 0).keys():
                if pygame.mixer and self.bark is not None:
                    self.bark.play()
                    enemy.knockbacked = True
                    if enemy.lives <= 0:
                        enemy.kill()
                        print("collide")


            pygame.draw.rect(self.screen, (0, 128, 255), pygame.Rect(30, 30, 60, 60))
            self.clock.tick(self.FPS)
            self.camera.scroll()

            self.enemy_group.draw(self.screen)
            self.player_group.draw(self.screen)
            self.window.blit(self.screen, (0,0))
            pygame.display.set_caption("current FPS: "+str(self.clock.get_fps()))
            pygame.display.update()




g = Game()
g.game_loop()

"""
import pygame

class Game():

    def __init__(self):
        pygame.init()
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 1280, 720
        self.display = pygame.Surface((self.DISPLAY_W,self.DISPLAY_H))
        self.window = pygame.display.set_mode(((self.DISPLAY_W,self.DISPLAY_H)))
        self.font = pygame.font.get_default_font()
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        # self.main_menu = mainMenu(self)
        # self.options = infoMenu(self)
        # self.combatGame = combatGame(self)
        # self.state = self.combatGame

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.state.run_display = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    def draw_text(self, text, size, x, y ):
        font = pygame.font.Font(self.font_name,size)
        text_surface = font.render(text, True, self.WHITE).convert_alpha()
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface,text_rect)

    def game_loop(self):
        while self.playing:
            self.check_events()
            if self.START_KEY:
                self.playing= False
            self.display.fill(self.BLACK)
            self.draw_text('Thanks for Playing', 20, self.DISPLAY_W/2, self.DISPLAY_H/2)

            pygame.display.update()
            self.reset_keys()

g = Game()

while g.running:
    # g.state.run()
    g.game_loop()

    """