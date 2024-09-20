import pygame

from camera import *
from title import Title
from animation import Animation
from intro1 import Intro1
from intro2 import Intro2
from diologue import Dialogue
from game import Game

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
        self.state = "game"
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








my_game = GameStateController()
my_game.main_loop()