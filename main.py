import pygame

from camera import *
from title import Title
from animation import Animation
from intro1 import Intro1
from intro2 import Intro2
from diologue import Dialogue
from game import Game
from slideshow import Slideshow

TOTAL_LIVES = 10
HP_WIDTH = 600
DISPLAY_W, DISPLAY_H = 1280, 720


pygame.mixer.pre_init()
pygame.init()

class GameStateController():
    "main main main"
    def __init__(self):

        pygame.mixer.music.load("assets/music/colyon-clip.ogg")
        pygame.mixer.music.set_volume(0.7)
        pygame.mixer.music.play(-1,0.0)
        
        self.woman_cry = pygame.mixer.Sound("assets/se/woman_cry.ogg")
        self.woman_can_cry = True
        self.woman_cry.set_volume(0.3)

        self.roar = pygame.mixer.Sound("assets/se/roar.ogg")
        self.can_roar = True
        self.roar.set_volume(0.3)

        self.screen = pygame.Surface((DISPLAY_W,DISPLAY_H))
        self.window = pygame.display.set_mode((DISPLAY_W,DISPLAY_H))

        self.title_screen = Title("assets/images/KH_Title.png")

        self.intro1 = Intro1(self.screen, 1)
        self.intro2 = Animation("assets/images/intro/2", self.screen)
        self.intro3 = Intro2(self.screen)
        self.intro4 = Animation("assets/images/intro/4", self.screen, 200, True)
        self.intro5 = Dialogue("assets/images/intro/5")
        self.intro6 = Dialogue("assets/images/intro/6")
        self.intro7 = Dialogue("assets/images/intro/7")
        self.intro8 = Slideshow("assets/images/intro/8", (0.5,1,1,1), 1000)
        self.intro9 = Animation("assets/images/intro/9", self.screen, 500, False)
        self.intro10 = Animation("assets/images/intro/10", self.screen, 200, False)
        self.intro11 = Animation("assets/images/intro/11", self.screen, 200, False)
        self.intro12 = Animation("assets/images/intro/12", self.screen, 400, False)




        self.level1 = Game(self.screen, self.window, 1)
        self.level2 = Game(self.screen, self.window, 2)
        self.level3 = Game(self.screen, self.window, 3)

        self.clock = pygame.time.Clock()
        self.state = "intro7"
        self.FPS = 60
        self.can_switch_music1 = True #fadeout
        self.can_switch_music2 = True #new music lions
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
            self.state = "level1"
        if self.level1.done:
            self.state = "intro6"
            if self.woman_can_cry:
                self.level1.bark.stop()
                self.woman_cry.play()
                self.woman_can_cry = False
        if self.intro6.done:
            self.state = "level2"
        if self.level2.done:
            self.state = "intro7"
            if self.can_switch_music1:
                pygame.mixer.music.fadeout(3000)
                self.can_switch_music1 = False
            
        if self.intro7.done:
            if self.can_switch_music2:
                pygame.mixer.stop()
                pygame.mixer.music.load("assets/music/kh-lion-long.ogg")
                pygame.mixer.music.set_volume(0.7)
                pygame.mixer.music.play(-1,0.0)
                self.can_switch_music2 = False
            self.state = "intro8"

        if self.intro8.done:
            self.state = "intro9"
        if not self.intro9.running:
            self.state = "intro10"
        if not self.intro10.running:
            self.state = "intro11"
        if not self.intro11.running:
            self.state = "intro12"
            if self.can_roar:
                self.roar.play()
                self.can_roar = False
        if not self.intro12.running:
            self.state = "level3"

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

            elif self.state == "level1":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.done = True
                    self.level1.check_events2(event)
                self.screen.fill((0,0,0))
                # if self.state == "game":
                self.level1.game_loop()

            elif self.state == "intro6":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.done = True
                    self.intro6.check_events(event)
                self.intro6.run(self.screen)

            elif self.state == "level2":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.done = True
                    self.level2.check_events2(event)
                self.screen.fill((0,0,0))
                self.level2.game_loop()

            elif self.state == "intro7":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.done = True
                    self.intro7.check_events(event)
                self.intro7.run(self.screen)

            elif self.state == "intro8":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.done = True
                    self.intro8.check_events(event)
                self.intro8.run(self.screen)

            elif self.state == "intro9":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.done = True
                    self.intro9.check_events(event)
                self.intro9.run()

            elif self.state == "intro10":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.done = True
                    self.intro10.check_events(event)
                self.intro10.run()

            elif self.state == "intro11":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.done = True
                    self.intro11.check_events(event)
                self.intro11.run()

            elif self.state == "intro12":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.done = True
                    self.intro12.check_events(event)
                self.intro12.run()

            elif self.state == "level3":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.done = True
                    self.level3.check_events2(event)
                self.screen.fill((0,0,0))
                # if self.state == "game":
                self.level3.game_loop()



            self.window.blit(self.screen, (0,0))
            self.clock.tick(self.FPS)
            pygame.display.update()
            pygame.display.set_caption("current FPS: "+str(self.clock.get_fps()))








my_game = GameStateController()
my_game.main_loop()