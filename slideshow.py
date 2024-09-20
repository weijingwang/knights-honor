import pygame
import os

# Initialize Pygame
pygame.init()

# Define constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60

class Slideshow:
    def __init__(self, image_folder, timings, fade_duration=200):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Slideshow")
        self.clock = pygame.time.Clock()
        self.images = self.load_images(image_folder)
        self.timings = timings
        self.fade_duration = fade_duration  # milliseconds for fade transition
        self.current_index = 0
        self.slide_start_time = pygame.time.get_ticks()
        self.fade_start_time = None
        self.fade_in_progress = False
        self.running = True

    def load_images(self, image_folder):
        """Load all images from the given folder, sort by name, and scale them to fit the screen."""
        images = []
        # List and sort the image files by name
        files = sorted([file for file in os.listdir(image_folder) if file.endswith((".png", ".jpg", ".jpeg", ".bmp"))])
        for file in files:
            img = pygame.image.load(os.path.join(image_folder, file))
            img = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
            images.append(img)
        return images

    def fade_transition(self, image1, image2, current_time):
        """Handles fading between two images with simultaneous fading out and in."""
        fade_progress = (current_time - self.fade_start_time) / self.fade_duration
        fade_progress = min(fade_progress, 1)  # Cap progress at 1 to avoid overflow

        # Fade out the current image
        image1.set_alpha(int((1 - fade_progress) * 255))
        self.screen.blit(image1, (0, 0))

        # Fade in the next image
        image2.set_alpha(int(fade_progress * 255))
        self.screen.blit(image2, (0, 0))

        pygame.display.flip()

    def run(self):
        """Main loop to run the slideshow."""
        while self.running:
            current_time = pygame.time.get_ticks()

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            current_image = self.images[self.current_index]
            next_image = self.images[(self.current_index + 1) % len(self.images)]

            # Check if it's time to transition to the next slide
            if not self.fade_in_progress and current_time - self.slide_start_time >= self.timings[self.current_index] * 1000:
                self.fade_start_time = pygame.time.get_ticks()
                self.fade_in_progress = True

            # If fade is in progress
            if self.fade_in_progress:
                self.fade_transition(current_image, next_image, current_time)

                # When fade completes, move to the next image
                if current_time - self.fade_start_time >= self.fade_duration:
                    self.fade_in_progress = False
                    self.current_index = (self.current_index + 1) % len(self.images)
                    self.slide_start_time = pygame.time.get_ticks()  # Reset slide timer

            # If no fade, just show the current image
            if not self.fade_in_progress:
                self.screen.blit(current_image, (0, 0))
                pygame.display.flip()

            self.clock.tick(FPS)

# Main function
def main():
    image_folder = "assets/images/intro/4"  # Folder with images
    # Set the timing for each slide (in seconds)
    timings = [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,]   # Example: each slide can have a different duration
    
    # Initialize and run the slideshow
    slideshow = Slideshow(image_folder, timings)
    
    if len(slideshow.images) > 0:
        slideshow.run()
    else:
        print("No images found in the folder.")

# Run the main function
if __name__ == "__main__":
    main()

# Quit pygame
pygame.quit()
