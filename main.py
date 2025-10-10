import pygame
import settings
import time

pygame.init()

# Gets the size of your screen for the pygame window
screen_info = pygame.display.Info()
screen_width, screen_height = screen_info.current_w, screen_info.current_h

# Calculates the size of the game based on desired grid size
game_width = settings.grid_size[0] * settings.GRID_SQUARE_SIZE + settings.BORDER_THICKNESS * 2
game_height = settings.grid_size[1] * settings.GRID_SQUARE_SIZE + settings.BORDER_THICKNESS * 2 + settings.INFO_BAR_HEIGHT

# Calculates where the top left corner is 
corner_x = screen_width / 2 - game_width / 2 
corner_y = screen_height / 2 - game_height / 2

# Calculates where the grid is going to start 
grid_start_postion_x = corner_x + settings.BORDER_THICKNESS
grid_start_positon_y = corner_y + settings.BORDER_THICKNESS + settings.INFO_BAR_HEIGHT

# Sets the pygame window size based on previously gathered values
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake")

# Function that generates the grid based on settings
def generate_grid():
    grid_width, grid_height = settings.grid_size[0], settings.grid_size[1]

    for x in range(grid_width):
        for y in range(grid_height):
            grid_position_x = grid_start_postion_x + x * settings.GRID_SQUARE_SIZE
            grid_position_y = grid_start_positon_y + y * settings.GRID_SQUARE_SIZE

            if (x + y) % 2 == 0:
                i = 0
            else:
                i = 1

            pygame.draw.rect(
                screen,
                settings.color_theme[i],
                (grid_position_x, grid_position_y, settings.GRID_SQUARE_SIZE, settings.GRID_SQUARE_SIZE),
            )


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 

    # Info bar
    pygame.draw.rect(
        screen,
        settings.color_theme[3],
        (corner_x, corner_y, game_width, game_height)
        )
    
    # Grid border
    pygame.draw.rect(
        screen, 
        settings.color_theme[2], 
        (corner_x, corner_y + settings.INFO_BAR_HEIGHT, game_width, game_height - settings.INFO_BAR_HEIGHT)
        ) 

    generate_grid()

    pygame.display.flip()



pygame.quit()