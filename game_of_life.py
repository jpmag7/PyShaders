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


zero = (0, 0, 0)
def apply_game_of_life():
    rows = len(matrix)
    cols = len(matrix[0])

    # Create a new matrix to store the next state
    new_matrix = [[0] * cols for _ in range(rows)]

    # Define the rules of the Game of Life
    def count_neighbors(x, y):
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                nx, ny = x + i, y + j
                if 0 <= nx < rows and 0 <= ny < cols and matrix[nx][ny] == 1:
                    count += 1
        return count

    for x in range(rows):
        for y in range(cols):
            neighbors = count_neighbors(x, y)

            # Apply the rules
            if matrix[x][y] == 1:  # Alive cell
                if neighbors < 2 or neighbors > 3:
                    new_matrix[x][y] = 0  # Dies due to underpopulation or overpopulation
                else:
                    new_matrix[x][y] = 1  # Survives
            else:  # Dead cell
                if neighbors == 3:
                    new_matrix[x][y] = 1  # Becomes alive due to reproduction

    return new_matrix


# Main loop
left_pressed_count = 0
frame_count = 0
locked = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                matrix = [
                    [0 for _ in range(WIDTH // PIXEL_SIZE)]  # Red pixels
                    for _ in range(HEIGHT // PIXEL_SIZE)
                ]
            elif event.key == pygame.K_a:
                locked = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                locked = False
        elif event.type == pygame.MOUSEBUTTONDOWN and locked:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            y, x = mouse_y // PIXEL_SIZE, mouse_x // PIXEL_SIZE
            if matrix[y][x] == 0:
                matrix[y][x] = 1
                pixel_array[x * PIXEL_SIZE : (x + 1) * PIXEL_SIZE, y * PIXEL_SIZE : (y + 1) * PIXEL_SIZE] = (255, 255, 255)
            else:
                matrix[y][x] = 0
                pixel_array[x * PIXEL_SIZE : (x + 1) * PIXEL_SIZE, y * PIXEL_SIZE : (y + 1) * PIXEL_SIZE] = (0, 0, 0)

    
    mouse_x, mouse_y = pygame.mouse.get_pos()
    left_button_pressed = pygame.mouse.get_pressed()[0]
    if left_button_pressed: left_pressed_count += 1
    else: left_pressed_count = 0
    
    if not locked and left_pressed_count > 1 and 0 < mouse_x < WIDTH and 0 < mouse_y < HEIGHT:
        y, x = mouse_y // PIXEL_SIZE, mouse_x // PIXEL_SIZE
        left_pressed_count = 0
        matrix[y][x] = 1
        pixel_array[x * PIXEL_SIZE : (x + 1) * PIXEL_SIZE, y * PIXEL_SIZE : (y + 1) * PIXEL_SIZE] = (255, 255, 255)

    frame_count += 1
    if frame_count >= 10 and not left_button_pressed and not locked:
        frame_count = 0
        # Clear the screen
        screen.fill((0, 0, 0))

        matrix = apply_game_of_life()

        # Render the matrix of pixels
        for y, row in enumerate(matrix):
            for x, state in enumerate(row):
                color = (255, 255, 255) if state == 1 else (0, 0, 0)
                pixel_array[x * PIXEL_SIZE : (x + 1) * PIXEL_SIZE, y * PIXEL_SIZE : (y + 1) * PIXEL_SIZE] = color

    # Update the display
    pygame.display.flip()

    # Control the frame rate (optional)
    pygame.time.Clock().tick(120)
