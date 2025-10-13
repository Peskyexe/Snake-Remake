import pygame
from pygame.math import Vector2
import settings

class Snake:
    def __init__(self):
        self.grid_pos = Vector2(settings.grid_size[0] // 2, settings.grid_size[1] // 2)
        self.real_pos = self.grid_pos * settings.GRID_SQUARE_SIZE
        self.direction =  Vector2(1, 0)
        self.target = self.grid_pos + self.direction
        self.turn_buffer = None

    def update(self, delte_time):

        # Calculaetes the target position and smoothly moves the snake to that position
        target_pixel = self.target * settings.GRID_SQUARE_SIZE
        self.real_pos = self.real_pos.lerp(target_pixel, min(1, delte_time * settings.SNAKE_SPEED))

        # Check if you've reached the target position
        if self.real_pos.distance_to(target_pixel) < 1:
            self.grid_pos = self.target
            
            if self.turn_buffer:
                # Snap to the grid position before turning
                self.real_pos = self.grid_pos * settings.GRID_SQUARE_SIZE
                self.direction = self.turn_buffer
                self.turn_buffer = None
            
            self.target = self.grid_pos + self.direction

    def turn(self, new_direction):
        # Only allow turning at or near the grid lines
        if (self.real_pos - self.grid_pos * settings.GRID_SQUARE_SIZE).length() < 1:
            self.direction = new_direction
            self.target = self.grid_pos + self.direction
        else:
            self.turn_buffer = new_direction

    def draw(self, surface):
        pygame.draw.rect(
            surface,
            (0, 255, 0),
            (self.real_pos.x, self.real_pos.y, settings.GRID_SQUARE_SIZE, settings.GRID_SQUARE_SIZE)
        )