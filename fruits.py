import settings
import pygame
from pygame.math import Vector2

class Fruit_1:
    def __init__(self, grid_pos):
        self.grid_pos = grid_pos
        self.value = settings.FRUIT_1_VALUE
        half = settings.GRID_SQUARE_SIZE / 2
        self.real_pos = self.grid_pos * settings.GRID_SQUARE_SIZE + Vector2(half, half)

    def draw(self, screen):
        # Draw a simple circle centered on the fruit's real_pos
        radius = settings.GRID_SQUARE_SIZE // 3
        pygame.draw.circle(screen, (255, 0, 0), (int(self.real_pos.x), int(self.real_pos.y)), radius)