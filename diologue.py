import os
import pygame

class Dialogue:
    def __init__(self, image_folder):
        self.image_folder = image_folder
        self.current_image_idx = 0
        self.done = False
        image_files = sorted([f for f in os.listdir(self.image_folder) if f.endswith(('png', 'jpg', 'jpeg'))])
        self.images = [pygame.image.load(os.path.join(self.image_folder, img)).convert_alpha() for img in image_files]
        self.image = self.images[self.current_image_idx]

    def run(self, screen):
        self.image = self.images[self.current_image_idx]

        screen.blit(self.image, (0, 0))

    def check_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if self.current_image_idx >= len(self.images)-1:
                    self.done = True
                else:
                    self.current_image_idx = (self.current_image_idx + 1) 


# https://freesound.org/people/Supercolio/sounds/355741/
