import pygame
import os

# Initialize Pygame
pygame.init()

# Define constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
FPS = 60

# Create the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Load images
def load_images(image_folder):
    images = []
    for file in os.listdir(image_folder):
        if file.endswith((".png", ".jpg", ".jpeg", ".bmp")):
            img = pygame.image.load(os.path.join(image_folder, file))
            img = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
            images.append(img)
    return images

# Fade between two images with simultaneous fading out and in
def fade_transition(image1, image2, fade_duration, current_time, start_time, screen):
    fade_progress = (current_time - start_time) / fade_duration
    if fade_progress > 1:
        fade_progress = 1  # Cap the progress to avoid overflow

    # Fade out the current image
    image1.set_alpha(int((1 - fade_progress) * 255))
    screen.blit(image1, (0, 0))

    # Fade in the next image
    image2.set_alpha(int(fade_progress * 255))
    screen.blit(image2, (0, 0))

    pygame.display.flip()

# Run slideshow
def run_slideshow(images, timings):
    clock = pygame.time.Clock()
    current_index = 0
    fade_duration = 2000  # milliseconds for fade transition
    slide_start_time = pygame.time.get_ticks()  # Start time for the first slide
    fade_start_time = None

    running = True
    fade_in_progress = False

    while running:
        current_time = pygame.time.get_ticks()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        current_image = images[current_index]
        next_image = images[(current_index + 1) % len(images)]

        # Check if it's time to transition to the next slide
        if not fade_in_progress and current_time - slide_start_time >= timings[current_index] * 1000:
            fade_start_time = pygame.time.get_ticks()
            fade_in_progress = True

        # If fade is in progress
        if fade_in_progress:
            fade_transition(current_image, next_image, fade_duration, current_time, fade_start_time, screen)

            # When fade completes, move to the next image
            if current_time - fade_start_time >= fade_duration:
                fade_in_progress = False
                current_index = (current_index + 1) % len(images)
                slide_start_time = pygame.time.get_ticks()  # Reset slide timer

        # If no fade, just show the current image
        if not fade_in_progress:
            screen.blit(current_image, (0, 0))
            pygame.display.flip()

        clock.tick(FPS)

# Main function
def main():
    image_folder = "images"  # Folder with images
    images = load_images(image_folder)
    
    # Set the timing for each slide (in seconds)
    timings = [1, 1, 1, 2]  # Example: each slide can have a different duration
    
    if len(images) > 0:
        run_slideshow(images, timings)
    else:
        print("No images found in the folder.")

# Run the main function
if __name__ == "__main__":
    main()

# Quit pygame
pygame.quit()
