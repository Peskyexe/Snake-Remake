import pygame
from pygame.math import Vector2
import settings

class Snake:
    def __init__(self):
        self.grid_pos = Vector2(settings.grid_size[0] // 2, settings.grid_size[1] // 2)
        self.real_pos = self.grid_pos * settings.GRID_SQUARE_SIZE
        self.direction =  Vector2(1, 0)
        self.target = self.grid_pos + self.direction
