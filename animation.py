import pygame
import os

class Animation:
    def __init__(self, image_folder, screen, delay_time=200, space_to_end = False):
        self.running = True
        self.screen = screen
        self.space_to_end = space_to_end
        # Settings
        self.delay_time = delay_time

        # Load images from a folder and sort them numerically
        self.image_folder = image_folder
        self.image_files = [f for f in os.listdir(self.image_folder) if f.endswith(('png', 'jpg', 'jpeg', 'bmp'))]
        self.image_files = sorted(self.image_files, key=self.numeric_sort_key)
        self.display_image(os.path.join(self.image_folder, self.image_files[0]))


        # Start with the first image
        self.current_image_index = 0
        self.last_switch_time = pygame.time.get_ticks()

    def check_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.running = False

    def numeric_sort_key(self, filename):
        # Sort images based on numeric value in the filename
        return int(os.path.splitext(filename)[0])

    def display_image(self, image_path):
        # Load and display the image
        image = pygame.image.load(image_path).convert_alpha()
        self.screen.blit(image, (0, 0))

    def run(self):
        # Get current time
        current_time = pygame.time.get_ticks()

        # Check if the delay time has passed
        if current_time - self.last_switch_time > self.delay_time:
            # Switch to the next image
            self.current_image_index += 1

            if self.current_image_index >= len(self.image_files):
                # Exit the loop when the slideshow finishes
                if not self.space_to_end:
                    self.running = False
                # print(self.running)
            else:
                # Display the next image
                image_path = os.path.join(self.image_folder, self.image_files[self.current_image_index])
                self.display_image(image_path)

                # Reset the last switch time
                self.last_switch_time = current_time

