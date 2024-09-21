import pygame
import random
from player import PlayerClass
from enemy import Enemy
from camera import *

TOTAL_LIVES = 10
HP_WIDTH = 600
DISPLAY_W, DISPLAY_H = 1280, 720

class Game():
    """basic game"""
    def __init__(self, screen, window, level):
        self.level = level
        if level == 1:
            self.enemy_count = 5
            self.enemy_image_path = "assets/images/KH_DOG.png"
        elif level == 2:
            self.enemy_count = 3
            self.enemy_image_path = "assets/images/KH_ENEMY.png"
        elif level == 3:
            self.enemy_count = 2
            self.enemy_image_path = "assets/images/KH_LION.png"

        self.screen = screen
        self.window = window
        self.bark = pygame.mixer.Sound("assets/se/dog_bark_clip.ogg")
        self.oof = pygame.mixer.Sound("assets/se/oof-clip.ogg")
        self.dogcry = pygame.mixer.Sound("assets/se/dogcry-clip.ogg")
        self.dogcry.set_volume(0.3)
        self.bark.set_volume(0.1)
        self.slash = pygame.mixer.Sound("assets/se/slash-clip.ogg")
        self.slash.set_volume(0.1)
        self.oof.set_volume(0.01)

        self.FPS = 60
        self.clock = pygame.time.Clock()

        self.font = pygame.font.get_default_font()
        self.amadis_frame = pygame.image.load("assets/images/amadis_frame.png").convert_alpha()

        self.bg1 = Background("assets/images/LANDSCAPEF.png")
        self.bg2 = Background("assets/images/KH_BG_1-2.png")
        self.bg3 = Background("assets/images/KH_BG_1-3.png")

        self.player = PlayerClass()

        self.all_sprites = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.background_group = pygame.sprite.Group()

        self.player_group.add(self.player)
        self.background_group.add(self.bg1)
        self.background_group.add(self.bg2)
        self.background_group.add(self.bg3)

        self.camera = Camera(self.player)

        self.HP_color = 'green'

        self.spawn_timer = 1 * self.FPS
        self.spawn_timer_store = self.spawn_timer
        self.max_spawn = 3
        self.spawn_location = 0
        self.done = False
        self.current_spawned = 0
        self.current_slain = 0

        # Variables for the death screen
        self.game_over = False
        self.death_screen = False

    def check_events(self):
        if self.death_screen:
            return  # Ignore other inputs when on the death screen
        
        self.player.K_LEFT = pygame.key.get_pressed()[pygame.K_LEFT]
        self.player.K_a = pygame.key.get_pressed()[pygame.K_a]
        self.player.K_RIGHT = pygame.key.get_pressed()[pygame.K_RIGHT]
        self.player.K_d = pygame.key.get_pressed()[pygame.K_d]

    def check_events2(self, event):
        if self.death_screen:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.respawn_player()
            return  # Ignore other inputs when on the death screen

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.player.is_jumping = True
            if event.key == pygame.K_SPACE:
                if self.player.can_attack:
                    self.slash.play()
                    self.player.attacking = True

    def spawn_enemies(self):
        if self.wait_time_done() and len(self.enemy_group) < self.max_spawn:
            if self.spawn_location:
                dogx = random.randrange(-500, -100)
            else:
                dogx = random.randrange(1280 * 2, 1280 * 2 + 300)
            dogx = dogx - self.camera.camera_offset_tracker.x
            dog = Enemy(dogx, self.enemy_image_path)
            self.enemy_group.add(dog)
            self.spawn_location = not self.spawn_location
            self.current_spawned += 1

    def wait_time_done(self):
        self.spawn_timer -= 1
        if self.spawn_timer <= 0:
            self.spawn_timer = self.spawn_timer_store
            return True
        else:
            return False

    def draw_HP_bar(self):
        if self.player.HP <= TOTAL_LIVES / 4:
            self.HP_color = "red"
        elif self.player.HP <= TOTAL_LIVES / 2:
            self.HP_color = "yellow"
        else:
            self.HP_color = "green"

        pygame.draw.rect(self.screen, (130, 3, 3), pygame.Rect(30, 30, HP_WIDTH, 15))
        pygame.draw.rect(self.screen, self.HP_color, pygame.Rect(30, 30, HP_WIDTH / TOTAL_LIVES * self.player.HP, 15))
        pygame.draw.rect(self.screen, (230, 230, 230), pygame.Rect(30, 33, HP_WIDTH / TOTAL_LIVES * self.player.HP, 2))
        pygame.draw.rect(self.screen, (200, 200, 200), pygame.Rect(30, 40, HP_WIDTH / TOTAL_LIVES * self.player.HP, 2))

    def draw_stamina_bar(self):
        pygame.draw.rect(self.screen, (80, 80, 80), pygame.Rect(30, 50, 300, 15))
        pygame.draw.rect(self.screen, (180, 180, 70),
                         pygame.Rect(30, 50, 300 / self.player.attack_cooldown_timer_store * self.player.attack_cooldown_timer, 15))

    def display_death_screen(self):
        """Draw the death screen"""
        self.screen.fill((0, 0, 0))
        font = pygame.font.SysFont(None, 72)
        text = font.render('You Died', True, (255, 0, 0))
        self.screen.blit(text, (DISPLAY_W // 2 - text.get_width() // 2, DISPLAY_H // 2 - 100))
        subtext = font.render('Press RETURN to respawn', True, (255, 255, 255))
        self.screen.blit(subtext, (DISPLAY_W // 2 - subtext.get_width() // 2, DISPLAY_H // 2))

    def respawn_player(self):
        """Respawn the player and reset the game state"""
        self.player.HP = TOTAL_LIVES
        self.enemy_group.empty()  # Remove all enemies
        self.current_slain = 0
        self.current_spawned = 0
        self.death_screen = False

    def game_loop(self):
        if self.death_screen:
            self.display_death_screen()
            return

        if self.current_slain >= self.enemy_count:
            self.done = True

        if self.current_slain + len(self.enemy_group) < self.enemy_count:
            self.spawn_enemies()

        self.check_events()

        self.background_group.draw(self.screen)
        self.background_group.update(self.camera.offset.x, self.camera.offset.y)

        self.player.rect.x = self.player.rect.x - self.camera.offset.x
        self.player.rect.y = self.player.rect.y - self.camera.offset.y
        self.player.update()

        for enemy in self.enemy_group:
            enemy.rect.x -= self.camera.offset.x
            enemy.rect.y -= self.camera.offset.y

        self.enemy_group.update(self.player_group, self.bg3.rect, self.camera.camera_offset_tracker, self.screen)

        for enemy in pygame.sprite.groupcollide(self.enemy_group, self.player_group, 0, 0).keys():
            if enemy.wait_time_done():
                enemy.attack_movement()
                enemy.oof.play()
                self.player.HP -= 1

            if self.player.attacking and self.player.damaging:
                enemy.knockbacked = True
                enemy.lives -= 1 * self.player.crit_multiplier
                if enemy.lives <= 1:
                    self.dogcry.play()
                    enemy.kill()
                    self.current_slain += 1
                else:
                    self.bark.play()

        if self.player.HP <= 0:
            self.death_screen = True

        self.enemy_group.draw(self.screen)
        self.player_group.draw(self.screen)

        self.screen.blit(self.amadis_frame, (0 - self.camera.camera_offset_tracker.x, 0))

        self.draw_HP_bar()
        self.draw_stamina_bar()

        self.camera.scroll(self.bg3.mostRighted, self.bg3.mostLefted)
