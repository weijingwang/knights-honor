import pygame


class Game():
    """basic game"""
    def __init__(self):
        pygame.mixer.pre_init()
        pygame.init()
        pygame.display.set_caption("knight's honor (pygame 38)")
        self.clock = pygame.time.Clock()
        self.DISPLAY_W = 1280
        self.DISPLAY_H = 720
        self.screen = pygame.display.set_mode((self.DISPLAY_W,self.DISPLAY_H))
        self.done = False

        self.bg1 = pygame.image.load("assets/images/KH_BG_1-1.png").convert_alpha()
        self.bg2 = pygame.image.load("assets/images/KH_BG_1-2.png").convert_alpha()
        self.bg3 = pygame.image.load("assets/images/KH_BG_1-3.png").convert_alpha()
        self.bg4 = pygame.image.load("assets/images/KH_BG_1-4.png").convert_alpha()

        pygame.mixer.music.load("assets/music/colyon-clip.ogg")
        pygame.mixer.music.play(-1,0.0)
        pygame.mixer.music.set_volume(0.5)

        

    def check_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                       self.done = True
    def game_loop(self):
        while not self.done:
            self.check_events()
            self.screen.blit(self.bg1, (0,0))
            self.screen.blit(self.bg2, (0,0))
            self.screen.blit(self.bg3, (0,0))
            self.screen.blit(self.bg4, (0,0))


            pygame.draw.rect(self.screen, (0, 128, 255), pygame.Rect(30, 30, 60, 60))
            self.screen.blit
            pygame.display.flip()




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