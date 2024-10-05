import pygame
import sys
import random
import colorsys

# Define constants
WIDTH, HEIGHT = 800, 600
PIXEL_SIZE = 5

# Initialize pygame
pygame.init()

# Create a window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pixel Matrix Renderer")

# Direct pixel array control
pixel_array = pygame.PixelArray(screen)

# Define a sample matrix of pixels (2D array of colors)
matrix = [
    [0 for _ in range(WIDTH // PIXEL_SIZE)]  # Red pixels
    for _ in range(HEIGHT // PIXEL_SIZE)
]

def generate_colors():
    colors = []
    for i in range(0, WIDTH // PIXEL_SIZE):
        hue = i / (WIDTH // PIXEL_SIZE)
        rgb = [int(c * 255) for c in colorsys.hsv_to_rgb(hue, 1.0, 1.0)]
        colors.append(tuple(rgb))
    return colors

# Generate a list of RGB colors
all_colors = generate_colors()
c_counter = 0
c_l = len(all_colors)

zero = (0, 0, 0)
def update_matrix(m):
    for y in reversed(range(HEIGHT // PIXEL_SIZE)):
        for x in range(WIDTH // PIXEL_SIZE):
            if y > 0 and m[y-1][x] == 1:
                color = pixel_array[x * PIXEL_SIZE : (x + 1) * PIXEL_SIZE, (y-1) * PIXEL_SIZE : y * PIXEL_SIZE]
                if m[y][x] == 0:
                    m[y][x] = 1
                    pixel_array[x * PIXEL_SIZE : (x + 1) * PIXEL_SIZE, y * PIXEL_SIZE : (y + 1) * PIXEL_SIZE] = color
                    m[y-1][x] = 0
                    pixel_array[x * PIXEL_SIZE : (x + 1) * PIXEL_SIZE, (y-1) * PIXEL_SIZE : y * PIXEL_SIZE] = zero
                elif x > 0 and m[y][x-1] == 0:
                    m[y][x-1] = 1
                    pixel_array[(x-1) * PIXEL_SIZE : x * PIXEL_SIZE, y * PIXEL_SIZE : (y + 1) * PIXEL_SIZE] = color
                    m[y-1][x] = 0
                    pixel_array[x * PIXEL_SIZE : (x + 1) * PIXEL_SIZE, (y-1) * PIXEL_SIZE : y * PIXEL_SIZE] = zero
                elif x < WIDTH//PIXEL_SIZE-1 and m[y][x+1] == 0:
                    m[y][x+1] = 1
                    pixel_array[(x+1) * PIXEL_SIZE : (x+2) * PIXEL_SIZE, y * PIXEL_SIZE : (y + 1) * PIXEL_SIZE] = color
                    m[y-1][x] = 0
                    pixel_array[x * PIXEL_SIZE : (x + 1) * PIXEL_SIZE, (y-1) * PIXEL_SIZE : y * PIXEL_SIZE] = zero


# Main loop
left_pressed_count = 0
screen.fill((0, 0, 0))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    mouse_x, mouse_y = pygame.mouse.get_pos()
    left_button_pressed = pygame.mouse.get_pressed()[0]
    if left_button_pressed: left_pressed_count += 1
    else: left_pressed_count = 0
    
    if left_pressed_count > 1 and 0 < mouse_x < WIDTH and 0 < mouse_y < HEIGHT:
        left_pressed_count = 0
        color = all_colors[c_counter]
        c_counter += 1
        c_counter = c_counter % c_l
        y, x = mouse_y // PIXEL_SIZE, mouse_x // PIXEL_SIZE
        pixel_array[x * PIXEL_SIZE : (x + 1) * PIXEL_SIZE, y * PIXEL_SIZE : (y + 1) * PIXEL_SIZE] = color
        matrix[y][x] = 1

    # Clear the screen
    #screen.fill((0, 0, 0))

    update_matrix(matrix)

    # Render the matrix of pixels
    #for y, row in enumerate(matrix):
    #    for x, state in enumerate(row):
    #        color = (0, 255, 0) if state else (0, 0, 0)
    #        pixel_array[x * PIXEL_SIZE : (x + 1) * PIXEL_SIZE, y * PIXEL_SIZE : (y + 1) * PIXEL_SIZE] = color

    

    # Update the display
    pygame.display.flip()

    # Control the frame rate (optional)
    pygame.time.Clock().tick(120)
