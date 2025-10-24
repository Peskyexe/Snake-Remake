import pygame
from pygame.math import Vector2
import settings
import snake
from score_controller import ScoreController

pygame.init()
pygame.font.init()

font = pygame.font.SysFont('Arial', 25)
clock = pygame.time.Clock()

player = snake.Snake()
score_ctrl = ScoreController()
button_rect = None

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
grid_start_position_x = corner_x + settings.BORDER_THICKNESS
grid_start_position_y = corner_y + settings.BORDER_THICKNESS + settings.INFO_BAR_HEIGHT

# Sets the pygame window size based on previously gathered values
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake")

# Function that generates the grid based on settings
def generate_grid():
    grid_width, grid_height = settings.grid_size[0], settings.grid_size[1]
    base_x = grid_start_position_x
    base_y = grid_start_position_y

    for x in range(grid_width):
        for y in range(grid_height):
            cell_x = base_x + x * settings.GRID_SQUARE_SIZE
            cell_y = base_y + y * settings.GRID_SQUARE_SIZE

            if (x + y) % 2 == 0:
                i = 0
            else:
                i = 1

            pygame.draw.rect(
                screen,
                settings.color_theme[i],
                (cell_x, cell_y, settings.GRID_SQUARE_SIZE, settings.GRID_SQUARE_SIZE),
            )


def restart_popup():
    # draw a semi-transparent overlay
    overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    # draw centered restart button
    button_w, button_h = 260, 72
    bx = int((screen_width - button_w) / 2)
    by = int((screen_height - button_h) / 2)
    button_rect = pygame.Rect(bx, by, button_w, button_h)
    pygame.draw.rect(screen, settings.color_theme[1], button_rect)
    pygame.draw.rect(screen, settings.color_theme[2], button_rect, 4)

    # text
    text = font.render("Restart", True, (255, 255, 255))
    tx = bx + int((button_w - text.get_width()) / 2)
    ty = by + int((button_h - text.get_height()) / 2)
    screen.blit(text, (tx, ty))

    return button_rect

def restart():
    player.reset()
    score_ctrl.reset()

running = True
while running:
    delta_time = clock.tick(60) / 1000  # Time in seconds since last frame (60 FPS cap)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if not player.is_dead:
                if event.key == pygame.K_UP:
                    player.turn(Vector2(0, -1))
                elif event.key == pygame.K_DOWN:
                    player.turn(Vector2(0, 1))
                elif event.key == pygame.K_LEFT:
                    player.turn(Vector2(-1, 0))
                elif event.key == pygame.K_RIGHT:
                    player.turn(Vector2(1, 0))
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # if dead and the restart button is visible, clicking it restarts
            if player.is_dead and button_rect is not None:
                mouse_pos = pygame.mouse.get_pos()
                if button_rect.collidepoint(mouse_pos):
                    restart()

    screen.fill((0, 0, 0))

    player.update(delta_time)
    score_ctrl.update(delta_time, player)
    

    relative_text = font.render(f"Relative pos: {player.relative_pos.x:.2f}, {player.relative_pos.y:.2f}", False, (255, 255, 255))
    real_text = font.render(f"Real pos: {player.real_pos.x:.2f}, {player.real_pos.y:.2f}", False, (255, 255, 255))
    grid_text = font.render(f"Grid pos: {player.grid_pos.x}, {player.grid_pos.y}", False, (255, 255, 255))
    dead_text = font.render(f"Dead: {player.is_dead}", False, (255, 0, 0))
    score_text = font.render(f"Score: {score_ctrl.score}", False, (255, 255, 0))

    screen.blit(relative_text, (20, 10))
    screen.blit(real_text, (20, 10 + relative_text.get_height()))
    screen.blit(grid_text, (20, (10 + relative_text.get_height() + real_text.get_height())))
    screen.blit(dead_text, (20, (10 + relative_text.get_height() + real_text.get_height() + grid_text.get_height())))
    screen.blit(score_text, (20, (10 + relative_text.get_height() + real_text.get_height() + grid_text.get_height() + dead_text.get_height())))

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
    player.draw(screen, Vector2(grid_start_position_x, grid_start_position_y))
    score_ctrl.draw(screen, Vector2(grid_start_position_x, grid_start_position_y))
    

    pygame.display.flip()



pygame.quit()