import pygame
vec = pygame.math.Vector2

SCREEN_LEFT_BOUNDx = 0
SCREEN_RIGHT_BOUNDx = 1280

class Background(pygame.sprite.Sprite):
    """background"""
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.mostRighted = False
        self.mostLefted = False
        

    def draw(self, screen):
        screen.blit(self.image, (0,0))
    def update(self, camera_offset_x, camera_offset_y):
        # print(self.rect.left, self.mostLefted)

        self.rect.x -= camera_offset_x
        self.rect.y -= camera_offset_y

        # if self.rect.left < 0 or self.rect.right > 1280:
        #     pass
        if self.rect.left >= 0:
            self.mostLefted = True
        else:
            self.mostLefted = False
            
        # elif self.rect.right <= 1280:
        #     self.mostRighted = True
        
class Camera:
    def __init__(self, player):
        self.player = player
        self.offset = vec(0, 0)
        self.offset_float = vec(0, 0)
        self.DISPLAY_W, self.DISPLAY_H = 1280, 720
        self.CONST = vec(-self.DISPLAY_W / 2 + player.rect.w / 2, -self.player.ground_y + 20)
    def scroll(self, mostRighted, mostLefted):
        
        self.offset_float.x += (self.player.rect.x - self.offset_float.x + self.CONST.x)
        self.offset_float.y += (self.player.rect.y - self.offset_float.y + self.CONST.y)
        self.offset.x, self.offset.y = int(self.offset_float.x), int(self.offset_float.y)
        if mostLefted:
            self.offset.x, self.offset.y = 0,0

        # print(self.player.rect.x, self.offset.x)
        # self.offset.x = min(self.offset.x, LEFT_BOUND)
        # self.offset.x = max(self.offset.x, RIGHT_BOUND)
        # self.offset.x = max(self.player.rect.x, self.offset.x)
        # self.offset.x = min(self.offset.x, self.player.rect.x +self.player.rect.width - self.DISPLAY_W)
        # print(self.offset.x, self.player.rect.x +self.player.rect.width - self.DISPLAY_W)