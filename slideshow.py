import pygame
import os

class Slideshow:
    def __init__(self, image_folder, timings, fade_duration=500):
        self.images = self.load_images(image_folder)
        self.timings = timings
        self.fade_duration = fade_duration  # milliseconds for fade transition
        self.current_index = 0
        self.slide_start_time = pygame.time.get_ticks()
        self.fade_start_time = None
        self.fade_in_progress = False
        self.done = False

    def load_images(self, image_folder):
        """Load all images from the given folder, sort by name, and scale them to fit the screen."""
        images = []
        # List and sort the image files by name
        files = sorted([file for file in os.listdir(image_folder) if file.endswith((".png", ".jpg", ".jpeg", ".bmp"))])
        for file in files:
            img = pygame.image.load(os.path.join(image_folder, file)).convert_alpha()
            images.append(img)
        return images
    
    def check_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.done = True

    def fade_transition(self, image1, image2, current_time, screen):
        """Handles fading between two images with simultaneous fading out and in."""
        fade_progress = (current_time - self.fade_start_time) / self.fade_duration
        fade_progress = min(fade_progress, 1)  # Cap progress at 1 to avoid overflow

        # Fade out the current image
        image1.set_alpha(int((1 - fade_progress) * 255))
        screen.blit(image1, (0, 0))

        # Fade in the next image
        image2.set_alpha(int(fade_progress * 255))
        screen.blit(image2, (0, 0))


    def run(self, screen):
        if self.current_index >= len(self.images) -1:
            self.done = True

        current_time = pygame.time.get_ticks()

        current_image = self.images[self.current_index]
        if self.current_index < len(self.images) - 1:
            next_image = self.images[self.current_index + 1]

            # Check if it's time to transition to the next slide
            if not self.fade_in_progress and current_time - self.slide_start_time >= self.timings[self.current_index] * 1000:
                self.fade_start_time = pygame.time.get_ticks()
                self.fade_in_progress = True

            # If fade is in progress
            if self.fade_in_progress:
                self.fade_transition(current_image, next_image, current_time, screen)

                # When fade completes, move to the next image
                if current_time - self.fade_start_time >= self.fade_duration:
                    self.fade_in_progress = False
                    self.current_index = (self.current_index + 1) % len(self.images)
                    self.slide_start_time = pygame.time.get_ticks()  # Reset slide timer

            # If no fade, just show the current image
            if not self.fade_in_progress:
                screen.blit(current_image, (0, 0))


# # Main function
# def main():
#     image_folder = "assets/images/intro/4"  # Folder with images
#     # Set the timing for each slide (in seconds)
#     timings = [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]   # Example: each slide can have a different duration
    
#     # Initialize and run the slideshow
#     slideshow = Slideshow(image_folder, timings)
    
#     if len(slideshow.images) > 0:
#         slideshow.run()
#     else:
#         print("No images found in the folder.")

# # Run the main function
# if __name__ == "__main__":
#     main()

# # Quit pygame
# pygame.quit()
