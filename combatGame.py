import pygame

class combatGame():
    """combat game"""
    def __init__(self, display):
        self.bg = pygame.image.load("assets/images/KH_BG_1-1.png").convert_alpha()
        self.display = display
    def run(self):
        self.display.blit(self.bg, (0,0))
        self.display.flip()
        
    def game_loop(self):
        while self.playing:
            self.check_events()
            if self.START_KEY:
                self.playing= False
            self.display.fill(self.BLACK)
            self.draw_text('Thanks for Playing', 20, self.DISPLAY_W/2, self.DISPLAY_H/2)

            pygame.display.update()
            self.reset_keys()
