import settings
import pygame
from pygame.math import Vector2


class Fruit_1:
    def __init__(self, grid_pos):
        # Store grid coordinates; actual pixel position is calculated when drawing
        self.grid_pos = grid_pos
        self.value = settings.FRUIT_1_VALUE
        half = settings.GRID_SQUARE_SIZE / 2
        # base pixel position relative to the grid origin (0,0)
        self._base_real_pos = self.grid_pos * settings.GRID_SQUARE_SIZE + Vector2(half, half)

    def draw(self, screen, offset=Vector2(0, 0)):
        # Draw a simple circle centered on the fruit's real_pos.
        # offset should be the top-left pixel coordinate of the grid in the window.
        real_pos = self._base_real_pos + offset
        radius = settings.GRID_SQUARE_SIZE // 3
        pygame.draw.circle(screen, (255, 0, 0), (int(real_pos.x), int(real_pos.y)), radius)


class Fruit_2:
    def __init__(self, grid_pos):
        # Store grid coordinates; actual pixel position is calculated when drawing
        self.grid_pos = grid_pos
        self.value = settings.FRUIT_2_VALUE
        half = settings.GRID_SQUARE_SIZE / 2
        # base pixel position relative to the grid origin (0,0)
        self._base_real_pos = self.grid_pos * settings.GRID_SQUARE_SIZE + Vector2(half, half)

    def draw(self, screen, offset=Vector2(0, 0)):
        # Draw a simple circle centered on the fruit's real_pos.
        # offset should be the top-left pixel coordinate of the grid in the window.
        real_pos = self._base_real_pos + offset
        radius = settings.GRID_SQUARE_SIZE // 3
        pygame.draw.circle(screen, (255, 255, 0), (int(real_pos.x), int(real_pos.y)), radius)