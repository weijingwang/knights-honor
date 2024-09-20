import pygame
import random
from player import PlayerClass
from enemy import Enemy
from camera import *
from title import Title
from animation import Animation
from intro1 import Intro1
from intro2 import Intro2
from diologue import Dialogue

TOTAL_LIVES = 10
HP_WIDTH = 600
DISPLAY_W, DISPLAY_H = 1280, 720
"dog cry from : https://freesound.org/people/jocelynlopez/sounds/635114/"
pygame.mixer.pre_init()
pygame.init()

class GameStateController():
    "main main main"
    def __init__(self):
        self.screen = pygame.Surface((DISPLAY_W,DISPLAY_H))
        self.window = pygame.display.set_mode((DISPLAY_W,DISPLAY_H))

        self.title_screen = Title("assets/images/KH_Title.png")
        # self.title_screen = Title("assets/images/dead.jpg")

        self.intro1 = Intro1(self.screen)
        self.intro2 = Animation("assets/images/intro/2", self.screen)
        self.intro3 = Intro2(self.screen)
        self.intro4 = Animation("assets/images/intro/4", self.screen, 200, True)
        self.intro5 = Dialogue("assets/images/intro/5")

        self.level1 = Game(self.screen, self.window, 1)
        self.clock = pygame.time.Clock()
        self.state = "title"
        self.FPS = 60

        self.done = False

    def update_state(self):
        if self.title_screen.done:
            self.state = "intro1"
        if self.intro1.done:
            self.state = "intro2"
        if not self.intro2.running:
            self.state = "intro3"
        if self.intro3.done:
            self.state = "intro4"
        if not self.intro4.running:
            self.state = "intro5"
        if self.intro5.done:
            self.state = "game"


    def main_loop(self):
        while not self.done:
            # print(self.state)
            self.update_state()

            if self.state == "title":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.done = True
                    self.title_screen.check_events(event)
                self.title_screen.run(self.screen)
            elif self.state == "intro1":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.done = True
                    self.intro1.check_events(event)

                self.intro1.update(self.screen)

            elif self.state == "intro2":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.done = True
                    self.intro2.check_events(event)

                self.intro2.run()

            elif self.state == "intro3":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.done = True
                    self.intro3.check_events(event)
                self.intro3.update(self.screen)

            elif self.state == "intro4":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.done = True
                    self.intro4.check_events(event)
                self.intro4.run()

            elif self.state == "intro5":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.done = True
                    self.intro5.check_events(event)
                self.intro5.run(self.screen)

            elif self.state == "game":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.done = True
                    self.level1.check_events2(event)
                self.screen.fill((0,0,0))
                # if self.state == "game":
                self.level1.game_loop()
            self.window.blit(self.screen, (0,0))
            self.clock.tick(self.FPS)
            pygame.display.update()
            pygame.display.set_caption("current FPS: "+str(self.clock.get_fps()))



class Game():
    """basic game"""
    def __init__(self, screen, window, level):
        self.level = level
        self.enemy_count = 5
        self.screen = screen
        self.window = window
        self.bark = pygame.mixer.Sound("assets/se/dog_bark_clip.ogg")
        self.oof = pygame.mixer.Sound("assets/se/oof-clip.ogg")
        self.dogcry = pygame.mixer.Sound("assets/se/dogcry-clip.ogg")
        self.dogcry.set_volume(0.5)
        self.bark.set_volume(0.3)
        self.slash = pygame.mixer.Sound("assets/se/slash-clip.ogg")
        self.slash.set_volume(0.6)
        self.oof.set_volume(0.6)

        self.FPS = 60
        # pygame.display.set_caption("knight's honor (pygame 38)")
        self.key = pygame.key.get_pressed()
        self.clock = pygame.time.Clock()
        
        self.K_LEFT, self.K_RIGHT, self.K_A, self.K_D, self.K_CLICK, self.K_SPACE = False, False, False, False, False, False



        self.font = pygame.font.get_default_font()
        self.amadis_frame = pygame.image.load("assets/images/amadis_frame.png").convert_alpha()

        self.bg1 = Background("assets/images/LANDSCAPEF.png")
        self.bg2 = Background("assets/images/KH_BG_1-2.png")
        self.bg3 = Background("assets/images/KH_BG_1-3.png")
        
        pygame.mixer.music.load("assets/music/colyon-clip.ogg")
        pygame.mixer.music.play(-1,0.0)
        pygame.mixer.music.set_volume(0.7)

        self.player = PlayerClass()

        self.all_sprites = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.background_group = pygame.sprite.Group()

        self.player_group.add(self.player)


        self.background_group.add(self.bg1)
        self.background_group.add(self.bg2)
        self.background_group.add(self.bg3)


        # self.all_sprites.add(self.player)
        # self.all_sprites.add(self.dog)
        # self.all_sprites.add(self.dog2)

        self.camera = Camera(self.player)

        self.HP_color = 'green'

        self.spawn_timer = 1 * self.FPS
        self.spawn_timer_store = self.spawn_timer
        self.max_spawn = 3

        self.spawn_location = 0



    def check_events(self):
        self.player.K_LEFT = pygame.key.get_pressed()[pygame.K_LEFT]
        self.player.K_a = pygame.key.get_pressed()[pygame.K_a]
        self.player.K_RIGHT = pygame.key.get_pressed()[pygame.K_RIGHT]
        self.player.K_d = pygame.key.get_pressed()[pygame.K_d]

    def check_events2(self, event):

        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     self.slash.play()
        #     self.player.attacking = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w: self.player.is_jumping = True
            if event.key == pygame.K_SPACE:
                self.slash.play()
                self.player.attacking = True
        #     # self.K_LEFT, self.K_RIGHT, self.K_A, self.K_D, self.K_CLICK, self.K_SPACE
        #     if event.key == pygame.K_LEFT: self.K_LEFT = True
        #     if event.key == pygame.K_BACKSPACE: self.BACK_KEY = True
        #     if event.key == pygame.K_DOWN: self.DOWN_KEY = True
        #     if event.key == pygame.K_UP: self.UP_KEY = True
        if event.type == pygame.KEYUP:
            pass
            # if event.key == pygame.K_BACKSPACE: self.BACK_KEY = True
        #     if event.key == pygame.K_DOWN: self.DOWN_KEY = True
        #     if event.key == pygame.K_UP: self.UP_KEY = True


    def spawn_enemies(self):
        if self.wait_time_done() and len(self.enemy_group) < self.max_spawn:
            if self.spawn_location:
                dogx = random.randrange(-500,-100)
            else:
                dogx = random.randrange(1280*2,1280*2+300)
            dogx = dogx  - self.camera.camera_offset_tracker.x # - 1280/2

            dog = Enemy(dogx)
            self.enemy_group.add(dog)
            print("enemy spawned at", dogx)
            self.spawn_location = not self.spawn_location



    def wait_time_done(self):
        self.spawn_timer -= 1
        if self.spawn_timer <= 0:
            self.spawn_timer= self.spawn_timer_store
            return True
        else:
            return False
        
    def draw_HP_bar(self):
        if self.player.HP <= TOTAL_LIVES/4:
            self.HP_color = "red"
        elif self.player.HP <= TOTAL_LIVES/2:
            self.HP_color = "yellow"
        else:
            self.HP_color = "green"
  
        pygame.draw.rect(self.screen, (130, 3, 3), pygame.Rect(30, 30, HP_WIDTH, 15))
        pygame.draw.rect(self.screen, self.HP_color, pygame.Rect(30, 30, HP_WIDTH/TOTAL_LIVES * self.player.HP, 15))
        pygame.draw.rect(self.screen, (230, 230, 230), pygame.Rect(30, 33, HP_WIDTH/TOTAL_LIVES * self.player.HP, 2))
        pygame.draw.rect(self.screen, (200, 200, 200), pygame.Rect(30, 40, HP_WIDTH/TOTAL_LIVES * self.player.HP, 2))


    def game_loop(self):
        self.spawn_enemies()
        
        self.check_events()

        self.background_group.draw(self.screen)
        self.background_group.update(self.camera.offset.x, self.camera.offset.y)
        
        self.player.rect.x = self.player.rect.x - self.camera.offset.x
        self.player.rect.y = self.player.rect.y - self.camera.offset.y

        self.player.update(self.enemy_group)

        for enemy in self.enemy_group:
            enemy.rect.x  -= self.camera.offset.x
            enemy.rect.y -= self.camera.offset.y

        self.enemy_group.update(self.player_group, self.bg3.rect, self.camera.camera_offset_tracker, self.screen) #use enemy group instead of updating individul enemy so that when enemy is killed, it is removed from group and not revived with the update function
        


#     canvas.blit(house, (0 - camera.offset.x, 0 - camera.offset.y))
# canvas.blit(cat.current_image,(cat.rect.x - camera.offset.x, cat.rect.y - camera.offset.y))
        # print(self.player.attack)

        for enemy in pygame.sprite.groupcollide(self.enemy_group, self.player_group, 0, 0).keys():
            
            if enemy.wait_time_done():
                enemy.attack_movement()
                enemy.oof.play()
                self.player.HP -= 1

            
            if pygame.mixer and self.bark is not None and self.player.attacking:
                self.player.attack = False
                self.player.image = self.player.image_left
                enemy.knockbacked = True
                enemy.lives -= 1*self.player.crit_multiplier
                if enemy.lives <= 1:
                    self.dogcry.play()
                    enemy.kill()
                    print("collide")
                else:
                    self.bark.play()

        # if self.player.HP <= 0:
        #     quit()
        # print(self.player.HP)


        self.enemy_group.draw(self.screen)
        self.player_group.draw(self.screen)

        
        self.screen.blit(self.amadis_frame, (0-self.camera.camera_offset_tracker.x,0))


        self.draw_HP_bar()

        self.camera.scroll(self.bg3.mostRighted, self.bg3.mostLefted)





my_game = GameStateController()
my_game.main_loop()