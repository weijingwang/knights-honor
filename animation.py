import pygame
import os

# Initialize pygame
pygame.init()

# Settings
screen_width = 1280  # Adjust screen width to match your image size
screen_height = 720  # Adjust screen height to match your image size
delay_time = 500  # Adjustable time (milliseconds) between slides (2 seconds)

# Create a screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Slideshow')

# Load images from a folder and sort them numerically
image_folder = "assets/images/intro"  # Replace with your image folder
image_files = [f for f in os.listdir(image_folder) if f.endswith(('png', 'jpg', 'jpeg', 'bmp'))]

# Sort images by their numeric value in the filename
def numeric_sort_key(filename):
    return int(os.path.splitext(filename)[0])

image_files = sorted(image_files, key=numeric_sort_key)

# Check if images are available
if not image_files:
    print("No images found in the folder.")
    pygame.quit()
    exit()

# Function to display an image
def display_image(image_path):
    image = pygame.image.load(image_path)
    image = pygame.transform.scale(image, (screen_width, screen_height))  # Resize image to fit screen
    screen.blit(image, (0, 0))
    pygame.display.update()

# Slideshow logic
def run_slideshow():
    current_image_index = 0
    last_switch_time = pygame.time.get_ticks()  # Get the current time in milliseconds

    running = True
    while running:
        # Handle events (such as quitting the program)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Get current time
        current_time = pygame.time.get_ticks()

        # Check if the delay time has passed
        if current_time - last_switch_time > delay_time:
            # Switch to the next image
            current_image_index += 1

            if current_image_index >= len(image_files):
                # Exit the loop when the slideshow finishes
                running = False
            else:
                # Display the next image
                image_path = os.path.join(image_folder, image_files[current_image_index])
                display_image(image_path)

                # Reset the last switch time
                last_switch_time = current_time

        # Limit the frame rate to make sure the program isn't using too much CPU
        pygame.time.Clock().tick(60)

    pygame.quit()

# Main loop
display_image(os.path.join(image_folder, image_files[0]))  # Display the first image
run_slideshow()
