import pygame
from pygame.math import Vector2
import settings

class Snake:
    def __init__(self):
        self.grid_pos = Vector2(settings.grid_size[0] // 2, settings.grid_size[1] // 2)
        self.real_pos = self.grid_pos * settings.GRID_SQUARE_SIZE
        self.direction =  Vector2(1, 0)
        self.turn_buffer = None

    def update(self, delta_time):
        self.real_pos = self.real_pos + settings.SNAKE_SPEED * self.direction * delta_time

    def turn(self, new_direction):
        pass

    def draw(self, surface, offset = Vector2(0, 0)):
        pygame.draw.rect(
            surface,
            (0, 255, 0),
            (self.real_pos.x + offset.x, self.real_pos.y + offset.y, settings.GRID_SQUARE_SIZE, settings.GRID_SQUARE_SIZE)
        )